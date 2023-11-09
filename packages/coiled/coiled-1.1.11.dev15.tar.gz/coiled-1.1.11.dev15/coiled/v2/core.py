from __future__ import annotations

import asyncio
import base64
import datetime
import json
import logging
import platform
import sys
import weakref
from collections import namedtuple
from hashlib import md5
from pathlib import Path
from typing import (
    Awaitable,
    BinaryIO,
    Callable,
    Generic,
    NoReturn,
    Union,
    cast,
    overload,
)

import backoff
import dask.config
import dask.distributed
import httpx
from aiohttp import ClientResponseError, ContentTypeError
from dask.utils import parse_timedelta
from distributed.utils import Log, Logs
from rich.progress import Progress
from typing_extensions import TypeAlias

from coiled.cli.setup.entry import do_setup_wizard
from coiled.context import track_context
from coiled.core import Async, IsAsynchronous, Sync, delete_docstring, list_docstring
from coiled.core import Cloud as OldCloud
from coiled.errors import ClusterCreationError, DoesNotExist, ServerError
from coiled.types import (
    ApproximatePackageRequest,
    ApproximatePackageResult,
    ArchitectureTypesEnum,
    AWSOptions,
    GCPOptions,
    PackageLevel,
    PackageSchema,
    ResolvedPackageInfo,
    SoftwareEnvironmentAlias,
)
from coiled.utils import (
    COILED_LOGGER_NAME,
    AsyncBytesIO,
    GatewaySecurity,
    get_grafana_url,
    validate_backend_options,
)

from .states import (
    InstanceStateEnum,
    ProcessStateEnum,
    flatten_log_states,
    get_process_instance_state,
    log_states,
)
from .widgets.util import simple_progress

logger = logging.getLogger(COILED_LOGGER_NAME)


def setup_logging(level=logging.INFO):
    # We want to be able to give info-level messages to users.
    # For users who haven't set up a log handler, this requires creating one (b/c the handler of "last resort,
    # logging.lastResort, has a level of "warning".
    #
    # Conservatively, we only do anything here if the user hasn't set up any log handlers on the root logger
    # or the Coiled logger. If they have any handler, we assume logging is configured how they want it.
    coiled_logger = logging.getLogger(COILED_LOGGER_NAME)
    root_logger = logging.getLogger()
    if coiled_logger.handlers == [] and root_logger.handlers == []:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(fmt="[%(asctime)s][%(levelname)-8s][%(name)s] %(message)s"))
        # Conservatively, only change the Coiled logger level there's no log level specified yet.
        if coiled_logger.level == 0:
            coiled_logger.setLevel(level)
            coiled_logger.addHandler(stream_handler)


async def handle_api_exception(response, exception_cls=ServerError) -> NoReturn:
    try:
        error_body = await response.json()
    except ContentTypeError:
        raise exception_cls(
            f"Unexpected status code ({response.status}) to {response.method}:{response.url}, contact support@coiled.io"
        )
    if "message" in error_body:
        raise exception_cls(error_body["message"])
    if "detail" in error_body:
        raise exception_cls(error_body["detail"])
    raise exception_cls(error_body)


CloudV2SyncAsync: TypeAlias = Union["CloudV2[Async]", "CloudV2[Sync]"]


class CloudV2(OldCloud, Generic[IsAsynchronous]):
    _recent_sync: list[weakref.ReferenceType[CloudV2[Sync]]] = list()
    _recent_async: list[weakref.ReferenceType[CloudV2[Async]]] = list()

    # just overriding to get the right signature (CloudV2, not Cloud)
    def __enter__(self: CloudV2[Sync]) -> CloudV2[Sync]:
        return self

    def __exit__(self: CloudV2[Sync], typ, value, tb) -> None:
        self.close()

    async def __aenter__(self: CloudV2[Async]) -> CloudV2[Async]:
        return await self._start()

    async def __aexit__(self: CloudV2[Async], typ, value, tb) -> None:
        await self._close()

    # these overloads are necessary for the typechecker to know that we really have a CloudV2, not a Cloud
    # without them, CloudV2.current would be typed to return a Cloud
    #
    # https://www.python.org/dev/peps/pep-0673/ would remove the need for this.
    # That PEP also mentions a workaround with type vars, which doesn't work for us because type vars aren't
    # subscribtable
    @overload
    @classmethod
    def current(cls, asynchronous: Sync) -> CloudV2[Sync]: ...

    @overload
    @classmethod
    def current(cls, asynchronous: Async) -> CloudV2[Async]: ...

    @overload
    @classmethod
    def current(cls, asynchronous: bool) -> CloudV2: ...

    @classmethod
    def current(cls, asynchronous: bool) -> CloudV2:
        recent: list[weakref.ReferenceType[CloudV2]]
        if asynchronous:
            recent = cls._recent_async
        else:
            recent = cls._recent_sync
        try:
            cloud = recent[-1]()
            while cloud is None or cloud.status != "running":
                recent.pop()
                cloud = recent[-1]()
        except IndexError:
            if asynchronous:
                return cls(asynchronous=True)
            else:
                return cls(asynchronous=False)
        else:
            return cloud

    @track_context
    async def _get_default_instance_types(self, provider: str, gpu: bool = False, arch: str = "x86_64") -> list[str]:
        if arch not in ("arm64", "x86_64"):
            raise ValueError(f"arch '{arch}' is not supported for default instance types")
        if provider == "aws":
            if arch == "arm64":
                if gpu:
                    return ["g5g.xlarge"]  # has NVIDIA T4G
                else:
                    return ["m7g.xlarge", "m6g.xlarge"]
            if gpu:
                return ["g4dn.xlarge"]
            else:
                return ["m6i.xlarge", "m5.xlarge"]
        elif provider == "gcp":
            if arch != "x86_64":
                raise ValueError(f"no default instance type for GCP with {arch} architecture")
            if gpu:
                # n1-standard-8 with 30GB of memory might be best, but that's big for a default
                return ["n1-standard-4"]
            else:
                return ["e2-standard-4"]
        else:
            raise ValueError(f"unexpected provider {provider}; cannot determine default instance types")

    async def _list_dask_scheduler_page(
        self,
        page: int,
        account: str | None = None,
        since: str | None = "7 days",
        user: str | None = None,
    ) -> tuple[list, bool]:
        page_size = 100
        account = account or self.default_account
        kwargs = {}
        if since:
            kwargs["since"] = parse_timedelta(since)
        if user:
            kwargs["user"] = user
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/analytics/{account}/clusters/list",
            params={
                "limit": page_size,
                "offset": page_size * page,
                **kwargs,
            },
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    @track_context
    async def _list_dask_scheduler(
        self,
        account: str | None = None,
        since: str | None = "7 days",
        user: str | None = None,
    ):
        return await self._depaginate_list(
            self._list_dask_scheduler_page,
            account=account,
            since=since,
            user=user,
        )

    @overload
    def list_dask_scheduler(
        self: Cloud[Sync],
        account: str | None = None,
        since: str | None = "7 days",
        user: str | None = None,
    ) -> list: ...

    @overload
    def list_dask_scheduler(
        self: Cloud[Async],
        account: str | None = None,
        since: str | None = "7 days",
        user: str | None = "",
    ) -> Awaitable[list]: ...

    def list_dask_scheduler(
        self,
        account: str | None = None,
        since: str | None = "7 days",
        user: str | None = "",
    ) -> list | Awaitable[list]:
        return self._sync(self._list_dask_scheduler, account, since=since, user=user)

    async def _list_computations(
        self, cluster_id: int | None = None, scheduler_id: int | None = None, account: str | None = None
    ):
        return await self._depaginate_list(
            self._list_computations_page, cluster_id=cluster_id, scheduler_id=scheduler_id, account=account
        )

    async def _list_computations_page(
        self,
        page: int,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
    ) -> tuple[list, bool]:
        page_size = 100
        account = account or self.default_account

        if not scheduler_id and not cluster_id:
            raise ValueError("either cluster_id or scheduler_id must be specified")

        api = (
            f"/api/v2/analytics/{account}/{scheduler_id}/computations/list"
            if scheduler_id
            else f"/api/v2/analytics/{account}/cluster/{cluster_id}/computations/list"
        )

        response = await self._do_request(
            "GET",
            self.server + api,
            params={"limit": page_size, "offset": page_size * page},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    @overload
    def list_computations(
        self: Cloud[Sync],
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
    ) -> list: ...

    @overload
    def list_computations(
        self: Cloud[Async],
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
    ) -> Awaitable[list]: ...

    def list_computations(
        self, cluster_id: int | None = None, scheduler_id: int | None = None, account: str | None = None
    ) -> list | Awaitable[list]:
        return self._sync(self._list_computations, cluster_id=cluster_id, scheduler_id=scheduler_id, account=account)

    @overload
    def list_exceptions(
        self,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        since: str | None = None,
        user: str | None = None,
    ) -> list: ...

    @overload
    def list_exceptions(
        self,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        since: str | None = None,
        user: str | None = None,
    ) -> Awaitable[list]: ...

    def list_exceptions(
        self,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        since: str | None = None,
        user: str | None = None,
    ) -> list | Awaitable[list]:
        return self._sync(
            self._list_exceptions,
            cluster_id=cluster_id,
            scheduler_id=scheduler_id,
            account=account,
            since=since,
            user=user,
        )

    async def _list_exceptions(
        self,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        since: str | None = None,
        user: str | None = None,
    ):
        return await self._depaginate_list(
            self._list_exceptions_page,
            cluster_id=cluster_id,
            scheduler_id=scheduler_id,
            account=account,
            since=since,
            user=user,
        )

    async def _list_exceptions_page(
        self,
        page: int,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        since: str | None = None,
        user: str | None = None,
    ) -> tuple[list, bool]:
        page_size = 100
        account = account or self.default_account
        kwargs = {}
        if since:
            kwargs["since"] = parse_timedelta(since)
        if user:
            kwargs["user"] = user
        if cluster_id:
            kwargs["cluster"] = cluster_id
        if scheduler_id:
            kwargs["scheduler"] = scheduler_id
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/analytics/{account}/exceptions/list",
            params={"limit": page_size, "offset": page_size * page, **kwargs},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    async def _list_events_page(
        self,
        page: int,
        cluster_id: int,
        account: str | None = None,
    ) -> tuple[list, bool]:
        page_size = 100
        account = account or self.default_account
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/analytics/{account}/{cluster_id}/events/list",
            params={"limit": page_size, "offset": page_size * page},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    async def _list_events(self, cluster_id: int, account: str | None = None):
        return await self._depaginate_list(self._list_events_page, cluster_id=cluster_id, account=account)

    def list_events(self, cluster_id: int, account: str | None = None) -> list | Awaitable[list]:
        return self._sync(self._list_events, cluster_id, account)

    async def _send_state(self, cluster_id: int, desired_status: str, account: str | None = None):
        account = account or self.default_account
        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/analytics/{account}/{cluster_id}/desired-state",
            json={"desired_status": desired_status},
        )
        if response.status >= 400:
            await handle_api_exception(response)

    def send_state(self, cluster_id: int, desired_status: str, account: str | None = None) -> None | Awaitable[None]:
        return self._sync(self._send_state, cluster_id, desired_status, account)

    @track_context
    async def _list_clusters(self, account: str | None = None, max_pages: int | None = None):
        return await self._depaginate_list(self._list_clusters_page, account=account, max_pages=max_pages)

    @overload
    def list_clusters(
        self: Cloud[Sync],
        account: str | None = None,
        max_pages: int | None = None,
    ) -> list: ...

    @overload
    def list_clusters(
        self: Cloud[Async],
        account: str | None = None,
        max_pages: int | None = None,
    ) -> Awaitable[list]: ...

    @list_docstring
    def list_clusters(self, account: str | None = None, max_pages: int | None = None) -> list | Awaitable[list]:
        return self._sync(self._list_clusters, account, max_pages=max_pages)

    async def _list_clusters_page(self, page: int, account: str | None = None) -> tuple[list, bool]:
        page_size = 100
        account = account or self.default_account
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{account}/",
            params={"limit": page_size, "offset": page_size * page},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    @staticmethod
    async def _depaginate_list(
        func: Callable[..., Awaitable[tuple[list, bool]]],
        max_pages: int | None = None,
        *args,
        **kwargs,
    ) -> list:
        results_all = []
        page = 0
        while True:
            kwargs["page"] = page
            results, next = await func(*args, **kwargs)
            results_all += results
            page += 1
            if (not results) or next is None:
                break
            # page is the number of pages we've already fetched (since 0-indexed)
            if max_pages and page >= max_pages:
                break
        return results_all

    @track_context
    async def _create_package_sync_env(
        self,
        packages: list[ResolvedPackageInfo],
        progress: Progress | None = None,
        account: str | None = None,
        gpu_enabled: bool = False,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        region_name: str | None = None,
    ) -> SoftwareEnvironmentAlias:
        account = account or self.default_account
        prepared_packages: list[PackageSchema] = []
        for pkg in packages:
            if pkg["sdist"] and pkg["md5"]:
                with simple_progress(f"Uploading {pkg['name']}", progress=progress):
                    file_id = await self._create_senv_package(
                        pkg["sdist"],
                        contents_md5=pkg["md5"],
                        account=account,
                        region_name=region_name,
                    )
            else:
                file_id = None
            prepared_packages.append(
                {
                    "name": pkg["name"],
                    "source": pkg["source"],
                    "channel": pkg["channel"],
                    "conda_name": pkg["conda_name"],
                    "specifier": pkg["specifier"],
                    "include": pkg["include"],
                    "client_version": pkg["client_version"],
                    "file": file_id,
                }
            )
        with simple_progress("Requesting package sync build", progress=progress):
            result = await self._create_software_environment_v2(
                senv={
                    "packages": prepared_packages,
                    "raw_pip": None,
                    "raw_conda": None,
                },
                account=account,
                architecture=architecture,
                gpu_enabled=gpu_enabled,
                region_name=region_name,
            )
        return result

    @track_context
    async def _create_senv_package(
        self,
        package_file: BinaryIO,
        contents_md5: str,
        account: str | None = None,
        region_name: str | None = None,
    ) -> int:
        package_name = Path(package_file.name).name
        logger.debug(f"Starting upload for {package_name}")
        package_bytes = package_file.read()
        # s3 expects the md5 to be base64 encoded
        wheel_md5 = base64.b64encode(md5(package_bytes).digest()).decode("utf-8")
        account = account or self.default_account

        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/software-environment/account/{account}/package-upload",
            json={
                "name": package_name,
                "md5": contents_md5,
                "wheel_md5": wheel_md5,
                "region_name": region_name,
            },
        )
        if response.status >= 400:
            await handle_api_exception(response)  # always raises exception, no return
        data = await response.json()
        if data["should_upload"]:
            num_bytes = len(package_bytes)
            await self._put_package(
                url=data["upload_url"],
                package_data=AsyncBytesIO(package_bytes),
                file_md5=wheel_md5,
                num_bytes=num_bytes,
            )
        else:
            logger.debug(f"{package_name} MD5 matches existing, skipping upload")
        return data["id"]

    @backoff.on_exception(
        backoff.expo,
        ClientResponseError,
        max_time=120,
        giveup=lambda error: cast(ClientResponseError, error).status < 500,
    )
    async def _put_package(self, url: str, package_data: AsyncBytesIO, file_md5: str, num_bytes: int):
        # can't use the default session as it has coiled auth headers
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.put(
                url=url,
                # content must be set to an iterable of bytes, rather than a
                # bytes object (like file.read()) because files >2GB need
                # to be sent in chunks to avoid an OverflowError in the
                # Python stdlib ssl module, and httpx will not chunk up a
                # bytes object automatically.
                content=package_data,
                headers={
                    "Content-Type": "binary/octet-stream",
                    "Content-Length": str(num_bytes),
                    "content-md5": file_md5,
                },
                timeout=60,
            )
            response.raise_for_status()

    @track_context
    async def _create_cluster(
        self,
        # todo: make name optional and pick one for them, like pre-declarative?
        # https://gitlab.com/coiled/cloud/-/issues/4305
        name: str,
        *,
        software_environment: str | None = None,
        senv_v2_id: int | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        scheduler_options: dict | None = None,
        account: str | None = None,
        workers: int = 0,
        environ: dict | None = None,
        tags: dict | None = None,
        dask_config: dict | None = None,
        scheduler_vm_types: list | None = None,
        gcp_worker_gpu_type: str | None = None,
        gcp_worker_gpu_count: int | None = None,
        worker_vm_types: list | None = None,
        worker_disk_size: int | None = None,
        worker_disk_throughput: int | None = None,
        scheduler_disk_size: int | None = None,
        backend_options: AWSOptions | (GCPOptions | dict) | None = None,
        use_scheduler_public_ip: bool | None = None,
        use_dashboard_https: bool | None = None,
        private_to_creator: bool | None = None,
        extra_worker_on_scheduler: bool | None = None,
        n_worker_specs_per_host: int | None = None,
    ) -> tuple[int, bool]:
        # TODO (Declarative): support these args, or decide not to
        # https://gitlab.com/coiled/cloud/-/issues/4305

        account = account or self.default_account
        account, name = self._normalize_name(
            name,
            context_account=account,
            allow_uppercase=True,
        )

        self._verify_account(account)

        data = {
            "name": name,
            "workers": workers,
            "worker_instance_types": worker_vm_types,
            "scheduler_instance_types": scheduler_vm_types,
            "worker_options": worker_options,
            "worker_class": worker_class,
            "worker_disk_size": worker_disk_size,
            "worker_disk_throughput": worker_disk_throughput,
            "scheduler_disk_size": scheduler_disk_size,
            "scheduler_options": scheduler_options,
            "environ": environ,
            "tags": tags,
            "dask_config": dask_config,
            "private_to_creator": private_to_creator,
            "env_id": senv_v2_id,
            "env_name": software_environment,
            "extra_worker_on_scheduler": extra_worker_on_scheduler,
            "n_worker_specs_per_host": n_worker_specs_per_host,
            "use_aws_creds_endpoint": dask.config.get("coiled.use_aws_creds_endpoint", False),
        }

        backend_options = backend_options if backend_options else {}

        if gcp_worker_gpu_type is not None:
            # for backwards compatibility with v1 options
            backend_options = {
                **backend_options,
                "worker_accelerator_count": gcp_worker_gpu_count or 1,
                "worker_accelerator_type": gcp_worker_gpu_type,
            }
        elif gcp_worker_gpu_count:
            # not ideal but v1 only supported T4 and `worker_gpu=1` would give you one
            backend_options = {
                **backend_options,
                "worker_accelerator_count": gcp_worker_gpu_count,
                "worker_accelerator_type": "nvidia-tesla-t4",
            }

        if use_scheduler_public_ip is False:
            if "use_dashboard_public_ip" not in backend_options:
                backend_options["use_dashboard_public_ip"] = False

        if use_dashboard_https is False:
            if "use_dashboard_https" not in backend_options:
                backend_options["use_dashboard_https"] = False

        if backend_options:
            # for backwards compatibility with v1 options
            if "region" in backend_options and "region_name" not in backend_options:
                backend_options["region_name"] = backend_options["region"]  # type: ignore
                del backend_options["region"]  # type: ignore
            if "zone" in backend_options and "zone_name" not in backend_options:
                backend_options["zone_name"] = backend_options["zone"]  # type: ignore
                del backend_options["zone"]  # type: ignore
            # firewall just lets you specify a single CIDR block to open for ingress
            # we want to support a list of ingress CIDR blocks
            if "firewall" in backend_options:
                backend_options["ingress"] = [backend_options.pop("firewall")]  # type: ignore

            # convert the list of ingress rules to the FirewallSpec expected server-side
            if "ingress" in backend_options:
                fw_spec = {"ingress": backend_options.pop("ingress")}
                backend_options["firewall_spec"] = fw_spec  # type: ignore

            validate_backend_options(backend_options)
            data["options"] = backend_options

        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/clusters/account/{account}/",
            json=data,
        )

        response_json = await response.json()

        if response.status >= 400:
            from .widgets import EXECUTION_CONTEXT

            if response_json.get("code") == "NO_CLOUD_SETUP":
                server_error_message = response_json.get("message")
                error_message = f"{server_error_message} or by running `coiled setup`"

                if EXECUTION_CONTEXT == "terminal":
                    # maybe not interactive so just raise
                    raise ClusterCreationError(error_message)
                else:
                    # interactive session so let's try running the cloud setup wizard
                    if await do_setup_wizard():
                        # the user setup their cloud backend, so let's try creating cluster again!
                        response = await self._do_request(
                            "POST",
                            self.server + f"/api/v2/clusters/account/{account}/",
                            json=data,
                        )
                        if response.status >= 400:
                            await handle_api_exception(response)  # always raises exception, no return
                        response_json = await response.json()
                    else:
                        raise ClusterCreationError(error_message)
            else:
                if "message" in response_json:
                    raise ServerError(response_json["message"])
                if "detail" in response_json:
                    raise ServerError(response_json["detail"])
                raise ServerError(response_json)

        return response_json["id"], response_json["existing"]

    @overload
    def create_cluster(
        self: Cloud[Sync],
        name: str,
        *,
        software: str | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        scheduler_options: dict | None = None,
        account: str | None = None,
        workers: int = 0,
        environ: dict | None = None,
        tags: dict | None = None,
        dask_config: dict | None = None,
        private_to_creator: bool | None = None,
        scheduler_vm_types: list | None = None,
        worker_gpu_type: str | None = None,
        worker_vm_types: list | None = None,
        worker_disk_size: int | None = None,
        worker_disk_throughput: int | None = None,
        scheduler_disk_size: int | None = None,
        backend_options: dict | (AWSOptions | GCPOptions) | None = None,
    ) -> tuple[int, bool]: ...

    @overload
    def create_cluster(
        self: Cloud[Async],
        name: str,
        *,
        software: str | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        scheduler_options: dict | None = None,
        account: str | None = None,
        workers: int = 0,
        environ: dict | None = None,
        tags: dict | None = None,
        dask_config: dict | None = None,
        private_to_creator: bool | None = None,
        scheduler_vm_types: list | None = None,
        worker_gpu_type: str | None = None,
        worker_vm_types: list | None = None,
        worker_disk_size: int | None = None,
        worker_disk_throughput: int | None = None,
        scheduler_disk_size: int | None = None,
        backend_options: dict | (AWSOptions | GCPOptions) | None = None,
    ) -> Awaitable[tuple[int, bool]]: ...

    def create_cluster(
        self,
        name: str,
        *,
        software: str | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        scheduler_options: dict | None = None,
        account: str | None = None,
        workers: int = 0,
        environ: dict | None = None,
        tags: dict | None = None,
        private_to_creator: bool | None = None,
        dask_config: dict | None = None,
        scheduler_vm_types: list | None = None,
        worker_gpu_type: str | None = None,
        worker_vm_types: list | None = None,
        worker_disk_size: int | None = None,
        worker_disk_throughput: int | None = None,
        scheduler_disk_size: int | None = None,
        backend_options: dict | (AWSOptions | GCPOptions) | None = None,
    ) -> tuple[int, bool] | Awaitable[tuple[int, bool]]:
        return self._sync(
            self._create_cluster,
            name=name,
            software_environment=software,
            worker_class=worker_class,
            worker_options=worker_options,
            scheduler_options=scheduler_options,
            account=account,
            workers=workers,
            environ=environ,
            tags=tags,
            dask_config=dask_config,
            private_to_creator=private_to_creator,
            scheduler_vm_types=scheduler_vm_types,
            worker_vm_types=worker_vm_types,
            gcp_worker_gpu_type=worker_gpu_type,
            worker_disk_size=worker_disk_size,
            worker_disk_throughput=worker_disk_throughput,
            scheduler_disk_size=scheduler_disk_size,
            backend_options=backend_options,
        )

    @track_context
    async def _delete_cluster(self, cluster_id: int, account: str | None = None) -> None:
        account = account or self.default_account

        route = f"/api/v2/clusters/account/{account}/id/{cluster_id}"

        response = await self._do_request_idempotent(
            "DELETE",
            self.server + route,
        )
        if response.status >= 400:
            await handle_api_exception(response)
        else:
            # multiple deletes sometimes fail if we don't await response here
            await response.json()
            logger.info(f"Cluster {cluster_id} deleted successfully.")

    @overload
    def delete_cluster(self: Cloud[Sync], cluster_id: int, account: str | None = None) -> None: ...

    @overload
    def delete_cluster(self: Cloud[Async], cluster_id: int, account: str | None = None) -> Awaitable[None]: ...

    @delete_docstring  # TODO: this docstring erroneously says "Name of cluster" when it really accepts an ID
    def delete_cluster(self, cluster_id: int, account: str | None = None) -> Awaitable[None] | None:
        return self._sync(self._delete_cluster, cluster_id, account)

    async def _get_cluster_state(self, cluster_id: int, account: str | None = None) -> dict:
        account = account or self.default_account
        response = await self._do_request(
            "GET", self.server + f"/api/v2/clusters/account/{account}/id/{cluster_id}/state"
        )
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    async def _get_cluster_details(self, cluster_id: int, account: str | None = None):
        account = account or self.default_account
        r = await self._do_request_idempotent(
            "GET", self.server + f"/api/v2/clusters/account/{account}/id/{cluster_id}"
        )
        if r.status >= 400:
            await handle_api_exception(r)
        return await r.json()

    def _get_cluster_details_synced(self, cluster_id: int, account: str | None = None):
        return self._sync(
            self._get_cluster_details,
            cluster_id=cluster_id,
            account=account,
        )

    def _cluster_grafana_url(self, cluster_id: int, account: str | None = None):
        """for internal Coiled use"""
        account = account or self.default_account
        details = self._sync(
            self._get_cluster_details,
            cluster_id=cluster_id,
            account=account,
        )

        return get_grafana_url(details, account=account, cluster_id=cluster_id)

    def cluster_details(self, cluster_id: int, account: str | None = None):
        details = self._sync(
            self._get_cluster_details,
            cluster_id=cluster_id,
            account=account,
        )
        state_keys = ["state", "reason", "updated"]

        def get_state(state: dict):
            return {k: v for k, v in state.items() if k in state_keys}

        def get_instance(instance):
            if instance is None:
                return None
            else:
                return {
                    "id": instance["id"],
                    "created": instance["created"],
                    "name": instance["name"],
                    "public_ip_address": instance["public_ip_address"],
                    "private_ip_address": instance["private_ip_address"],
                    "current_state": get_state(instance["current_state"]),
                }

        def get_process(process: dict):
            if process is None:
                return None
            else:
                return {
                    "created": process["created"],
                    "name": process["name"],
                    "current_state": get_state(process["current_state"]),
                    "instance": get_instance(process["instance"]),
                }

        return {
            "id": details["id"],
            "name": details["name"],
            "workers": [get_process(w) for w in details["workers"]],
            "scheduler": get_process(details["scheduler"]),
            "current_state": get_state(details["current_state"]),
            "created": details["created"],
        }

    async def _get_workers_page(self, cluster_id: int, page: int, account: str | None = None) -> tuple[list, bool]:
        page_size = 100
        account = account or self.default_account

        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/workers/account/{account}/cluster/{cluster_id}/",
            params={"limit": page_size, "offset": page_size * page},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    @track_context
    async def _get_worker_names(
        self,
        account: str,
        cluster_id: int,
        statuses: list[ProcessStateEnum] | None = None,
    ) -> set[str]:
        worker_infos = await self._depaginate_list(self._get_workers_page, cluster_id=cluster_id, account=account)
        logger.debug(f"workers: {worker_infos}")
        return {w["name"] for w in worker_infos if statuses is None or w["current_state"]["state"] in statuses}

    @track_context
    async def _security(self, cluster_id: int, account: str | None = None):
        cluster = await self._get_cluster_details(cluster_id=cluster_id, account=account)
        if ProcessStateEnum(cluster["scheduler"]["current_state"]["state"]) != ProcessStateEnum.started:
            raise RuntimeError(f"Cannot get security info for cluster {cluster_id} scheduler is ready")

        public_ip = cluster["scheduler"]["instance"]["public_ip_address"]
        private_ip = cluster["scheduler"]["instance"]["private_ip_address"]
        tls_cert = cluster["cluster_options"]["tls_cert"]
        tls_key = cluster["cluster_options"]["tls_key"]
        scheduler_port = cluster["scheduler_port"]
        dashboard_address = cluster["scheduler"]["dashboard_address"]

        # TODO (Declarative): pass extra_conn_args if we care about proxying through Coiled to the scheduler
        security = GatewaySecurity(tls_key, tls_cert)

        return security, {
            "private_address": f"tls://{private_ip}:{scheduler_port}",
            "public_address": f"tls://{public_ip}:{scheduler_port}",
            "dashboard_address": dashboard_address,
        }

    @track_context
    async def _requested_workers(self, cluster_id: int, account: str | None = None) -> set[str]:
        raise NotImplementedError("TODO")

    @overload
    def requested_workers(self: Cloud[Sync], cluster_id: int, account: str | None = None) -> set[str]: ...

    @track_context
    async def _get_cluster_by_name(self, name: str, account: str | None = None) -> int:
        account, name = self._normalize_name(
            name, context_account=account, allow_uppercase=True, property_name="cluster name"
        )

        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{account}/name/{name}",
        )
        if response.status == 404:
            raise DoesNotExist
        elif response.status >= 400:
            await handle_api_exception(response)

        cluster = await response.json()
        return cluster["id"]

    @overload
    def get_cluster_by_name(
        self: Cloud[Sync],
        name: str,
        account: str | None = None,
    ) -> int: ...

    @overload
    def get_cluster_by_name(
        self: Cloud[Async],
        name: str,
        account: str | None = None,
    ) -> Awaitable[int]: ...

    def get_cluster_by_name(
        self,
        name: str,
        account: str | None = None,
    ) -> int | Awaitable[int]:
        return self._sync(
            self._get_cluster_by_name,
            name=name,
            account=account,
        )

    @track_context
    async def _cluster_status(
        self,
        cluster_id: int,
        account: str | None = None,
        exclude_stopped: bool = True,
    ) -> dict:
        raise NotImplementedError("TODO?")

    @track_context
    async def _get_cluster_states_declarative(
        self,
        cluster_id: int,
        account: str | None = None,
        start_time: datetime.datetime | None = None,
    ) -> int:
        account = account or self.default_account

        params = {"start_time": start_time.isoformat()} if start_time is not None else {}

        response = await self._do_request_idempotent(
            "GET",
            self.server + f"/api/v2/clusters/account/{account}/id/{cluster_id}/states",
            params=params,
        )
        if response.status >= 400:
            await handle_api_exception(response)

        return await response.json()

    def get_cluster_states(
        self,
        cluster_id: int,
        account: str | None = None,
        start_time: datetime.datetime | None = None,
    ) -> int | Awaitable[int]:
        return self._sync(
            self._get_cluster_states_declarative,
            cluster_id=cluster_id,
            account=account,
            start_time=start_time,
        )

    def get_clusters_by_name(
        self,
        name: str,
        account: str | None = None,
    ) -> list[dict]:
        """Get all clusters matching name."""
        return self._sync(
            self._get_clusters_by_name,
            name=name,
            account=account,
        )

    @track_context
    async def _get_clusters_by_name(self, name: str, account: str | None = None) -> list[dict]:
        account, name = self._normalize_name(name, context_account=account, allow_uppercase=True)

        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{account}",
            params={"name": name},
        )
        if response.status == 404:
            raise DoesNotExist
        elif response.status >= 400:
            await handle_api_exception(response)

        cluster = await response.json()
        return cluster

    @overload
    def cluster_logs(
        self: Cloud[Sync],
        cluster_id: int,
        account: str | None = None,
        scheduler: bool = True,
        workers: bool = True,
        errors_only: bool = False,
    ) -> Logs: ...

    @overload
    def cluster_logs(
        self: Cloud[Async],
        cluster_id: int,
        account: str | None = None,
        scheduler: bool = True,
        workers: bool = True,
        errors_only: bool = False,
    ) -> Awaitable[Logs]: ...

    @track_context
    async def _cluster_logs(
        self,
        cluster_id: int,
        account: str | None = None,
        scheduler: bool = True,
        workers: bool = True,
        errors_only: bool = False,
    ) -> Logs:
        def is_errored(process):
            process_state, instance_state = get_process_instance_state(process)
            return process_state == ProcessStateEnum.error or instance_state == InstanceStateEnum.error

        account = account or self.default_account

        # hits endpoint in order to get scheduler and worker instance names
        cluster_info = await self._get_cluster_details(cluster_id=cluster_id, account=account)

        try:
            scheduler_name = cluster_info["scheduler"]["instance"]["name"]
        except (TypeError, KeyError):
            # no scheduler instance name in cluster info
            logger.warning("No scheduler found when attempting to retrieve cluster logs.")
            scheduler_name = None

        worker_names = [
            worker["instance"]["name"]
            for worker in cluster_info["workers"]
            if worker["instance"] and (not errors_only or is_errored(worker))
        ]

        LabeledInstance = namedtuple("LabeledInstance", ("name", "label"))

        instances = []
        if scheduler and scheduler_name and (not errors_only or is_errored(cluster_info["scheduler"])):
            instances.append(LabeledInstance(scheduler_name, "Scheduler"))
        if workers and worker_names:
            instances.extend([LabeledInstance(worker_name, worker_name) for worker_name in worker_names])

        async def instance_log_with_semaphor(semaphor, **kwargs):
            async with semaphor:
                return await self._instance_logs(**kwargs)

        # only get 100 logs at a time; the limit here is redundant since aiohttp session already limits concurrent
        # connections but let's be safe just in case
        semaphor = asyncio.Semaphore(value=100)
        results = await asyncio.gather(
            *[
                instance_log_with_semaphor(semaphor=semaphor, account=account, instance_name=inst.name)
                for inst in instances
            ]
        )

        out = {
            instance_label: instance_log
            for (_, instance_label), instance_log in zip(instances, results)
            if len(instance_log)
        }

        return Logs(out)

    def cluster_logs(
        self,
        cluster_id: int,
        account: str | None = None,
        scheduler: bool = True,
        workers: bool = True,
        errors_only: bool = False,
    ) -> Logs | Awaitable[Logs]:
        return self._sync(
            self._cluster_logs,
            cluster_id=cluster_id,
            account=account,
            scheduler=scheduler,
            workers=workers,
            errors_only=errors_only,
        )

    async def _instance_logs(self, account: str, instance_name: str, safe=True) -> Log:
        response = await self._do_request(
            "GET",
            self.server + "/api/v2/instances/{}/instance/{}/logs".format(account, instance_name),
        )
        if response.status >= 400:
            if safe:
                logger.warning(f"Error retrieving logs for {instance_name}")
                return Log()
            await handle_api_exception(response)

        data = await response.json()

        messages = "\n".join(logline.get("message", "") for logline in data)

        return Log(messages)

    @overload
    def requested_workers(self: Cloud[Async], cluster_id: int, account: str | None = None) -> Awaitable[set[str]]: ...

    def requested_workers(self, cluster_id: int, account: str | None = None) -> set[str] | Awaitable[set[str]]:
        return self._sync(self._requested_workers, cluster_id, account)

    @overload
    def scale_up(self: Cloud[Sync], cluster_id: int, n: int, account: str | None = None) -> dict | None: ...

    @overload
    def scale_up(self: Cloud[Async], cluster_id: int, n: int, account: str | None = None) -> Awaitable[dict | None]: ...

    def scale_up(self, cluster_id: int, n: int, account: str | None = None) -> dict | None | Awaitable[dict | None]:
        """Scale cluster to ``n`` workers

        Parameters
        ----------
        cluster_id
            Unique cluster identifier.
        n
            Number of workers to scale cluster size to.
        account
            Name of Coiled account which the cluster belongs to.
            If not provided, will default to ``Cloud.default_account``.

        """
        return self._sync(self._scale_up, cluster_id, n, account)

    @overload
    def scale_down(
        self: Cloud[Sync],
        cluster_id: int,
        workers: set[str],
        account: str | None = None,
    ) -> None: ...

    @overload
    def scale_down(
        self: Cloud[Async],
        cluster_id: int,
        workers: set[str],
        account: str | None = None,
    ) -> Awaitable[None]: ...

    def scale_down(self, cluster_id: int, workers: set[str], account: str | None = None) -> Awaitable[None] | None:
        """Scale cluster to ``n`` workers

        Parameters
        ----------
        cluster_id
            Unique cluster identifier.
        workers
            Set of workers to scale down to.
        account
            Name of Coiled account which the cluster belongs to.
            If not provided, will default to ``Cloud.default_account``.

        """
        return self._sync(self._scale_down, cluster_id, workers, account)

    @track_context
    async def _better_cluster_logs(
        self,
        cluster_id: int,
        account: str | None = None,
        instance_ids: list[int] | None = None,
        dask: bool = False,
        system: bool = False,
        since_ms: int | None = None,
        until_ms: int | None = None,
        filter: str | None = None,
    ):
        account = account or self.default_account

        url_params = {}
        if dask:
            url_params["dask"] = "True"
        if system:
            url_params["system"] = "True"
        if since_ms:
            url_params["since_ms"] = f"{since_ms}"
        if until_ms:
            url_params["until_ms"] = f"{until_ms}"
        if filter:
            url_params["filter_pattern"] = f"{filter}"
        if instance_ids:
            url_params["instance_ids"] = ",".join(map(str, instance_ids))

        url_path = f"/api/v2/clusters/account/{account}/id/{cluster_id}/better-logs"

        response = await self._do_request(
            "GET",
            f"{self.server}{url_path}",
            params=url_params,
        )
        if response.status >= 400:
            await handle_api_exception(response)

        data = await response.json()

        return data

    def better_cluster_logs(
        self,
        cluster_id: int,
        account: str | None = None,
        instance_ids: list[int] | None = None,
        dask: bool = False,
        system: bool = False,
        since_ms: int | None = None,
        until_ms: int | None = None,
        filter: str | None = None,
    ) -> Logs:
        return self._sync(
            self._better_cluster_logs,
            cluster_id=cluster_id,
            account=account,
            instance_ids=instance_ids,
            dask=dask,
            system=system,
            since_ms=since_ms,
            until_ms=until_ms,
            filter=filter,
        )

    @track_context
    async def _scale_up(self, cluster_id: int, n: int, account: str | None = None, reason: str | None = None) -> dict:
        """
        Increases the number of workers by ``n``.
        """
        account = account or self.default_account
        data = {"n_workers": n}
        if reason:
            # pyright is annoying
            data["reason"] = reason  # type: ignore
        response = await self._do_request(
            "POST", f"{self.server}/api/v2/workers/account/{account}/cluster/{cluster_id}/", json=data
        )
        if response.status >= 400:
            await handle_api_exception(response)

        workers_info = await response.json()

        return {"workers": {w["name"] for w in workers_info}}

    @track_context
    async def _scale_down(
        self, cluster_id: int, workers: set[str], account: str | None = None, reason: str | None = None
    ) -> None:
        account = account or self.default_account

        reason_dict = {"reason": reason} if reason else {}
        response = await self._do_request(
            "DELETE",
            f"{self.server}/api/v2/workers/account/{account}/cluster/{cluster_id}/",
            params={"name": workers, **reason_dict},
        )
        if response.status >= 400:
            await handle_api_exception(response)

    @overload
    def security(
        self: Cloud[Sync], cluster_id: int, account: str | None = None
    ) -> tuple[dask.distributed.Security, dict]: ...

    @overload
    def security(
        self: Cloud[Async], cluster_id: int, account: str | None = None
    ) -> Awaitable[tuple[dask.distributed.Security, dict]]: ...

    def security(
        self, cluster_id: int, account: str | None = None
    ) -> tuple[dask.distributed.Security, dict] | Awaitable[tuple[dask.distributed.Security, dict]]:
        return self._sync(self._security, cluster_id, account)

    @track_context
    async def _fetch_package_levels(self) -> list[PackageLevel]:
        pass
        response = await self._do_request(
            "GET",
            f"{self.server}/api/v2/packages/",
        )
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    def get_ssh_key(
        self,
        cluster_id: int,
        account: str | None = None,
        worker: str | None = None,
    ) -> dict:
        account = account or self.default_account
        return self._sync(
            self._get_ssh_key,
            cluster_id=cluster_id,
            account=account,
            worker=worker,
        )

    @track_context
    async def _get_ssh_key(self, cluster_id: int, account: str, worker: str | None) -> dict:
        account = account or self.default_account

        route = f"/api/v2/clusters/account/{account}/id/{cluster_id}/ssh-key"
        url = f"{self.server}{route}"

        response = await self._do_request("GET", url, params={"worker": worker} if worker else None)
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    def get_cluster_log_info(
        self,
        cluster_id: int,
        account: str | None = None,
    ) -> dict:
        account = account or self.default_account
        return self._sync(
            self._get_cluster_log_info,
            cluster_id=cluster_id,
            account=account,
        )

    @track_context
    async def _get_cluster_log_info(
        self,
        cluster_id: int,
        account: str,
    ) -> dict:
        account = account or self.default_account

        route = f"/api/v2/clusters/account/{account}/id/{cluster_id}/log-info"
        url = f"{self.server}{route}"

        response = await self._do_request("GET", url)
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    def approximate_packages(self, package: list[ApproximatePackageRequest], architecture: ArchitectureTypesEnum):
        return self._sync(self._approximate_packages, package, architecture)

    @track_context
    async def _approximate_packages(
        self, packages: list[ApproximatePackageRequest], architecture: ArchitectureTypesEnum
    ) -> list[ApproximatePackageResult]:
        response = await self._do_request(
            "POST",
            f"{self.server}/api/v2/software-environment/approximate-packages",
            json={
                "architecture": architecture,
                "packages": packages,
                "metadata": {
                    "base_prefix": sys.base_prefix,
                    "platform": platform.platform(),
                    "prefix": sys.prefix,
                    "sys_path": sys.path,
                },
            },
        )
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    @track_context
    async def _get_cluster_aggregated_metric(
        self,
        cluster_id: int,
        account: str | None,
        query: str,
        over_time: str,
        start_ts: int | None,
        end_ts: int | None,
    ):
        account = account or self.default_account
        route = f"/api/v2/metrics/account/{account}/cluster/{cluster_id}/value"
        url = f"{self.server}{route}"
        params = {"query": query, "over_time": over_time}
        if start_ts:
            params["start_ts"] = str(start_ts)
        if end_ts:
            params["end_ts"] = str(end_ts)

        response = await self._do_request("GET", url, params=params)
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    @track_context
    async def _add_cluster_span(self, cluster_id: int, account: str | None, span_identifier: str, data: dict):
        account = account or self.default_account
        route = f"/api/v2/analytics/{account}/cluster/{cluster_id}/span/{span_identifier}"
        url = f"{self.server}{route}"

        response = await self._do_request("POST", url, json=data)
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    def _sync_request(self, route, method: str = "GET", json: bool = False, **kwargs):
        url = f"{self.server}{route}"
        response = self._sync(self._do_request, url=url, method=method, **kwargs)
        if response.status >= 400:
            raise ServerError(f"{url} returned {response.status}")

        async def get_result(r):
            return await r.json() if json else r.text()

        return self._sync(
            get_result,
            response,
        )


Cloud = CloudV2


def cluster_logs(
    cluster_id: int,
    account: str | None = None,
    scheduler: bool = True,
    workers: bool = True,
    errors_only: bool = False,
):
    """
    Returns cluster logs as a dictionary, with a key for the scheduler and each worker.

    .. versionchanged:: 0.2.0
       ``cluster_name`` is no longer accepted, use ``cluster_id`` instead.
    """
    with Cloud() as cloud:
        return cloud.cluster_logs(cluster_id, account, scheduler, workers, errors_only)


def better_cluster_logs(
    cluster_id: int,
    account: str | None = None,
    instance_ids: list[int] | None = None,
    dask: bool = False,
    system: bool = False,
    since_ms: int | None = None,
    until_ms: int | None = None,
    filter: str | None = None,
):
    """
    Pull logs for the cluster using better endpoint.

    Logs for recent clusters are split between system and container (dask), you can get
    either or both (or none).

    since_ms and until_ms are both inclusive (you'll get logs with timestamp matching those).
    """
    with Cloud() as cloud:
        return cloud.better_cluster_logs(
            cluster_id,
            account,
            instance_ids=instance_ids,
            dask=dask,
            system=system,
            since_ms=since_ms,
            until_ms=until_ms,
            filter=filter,
        )


def cluster_details(
    cluster_id: int,
    account: str | None = None,
) -> dict:
    """
    Get details of a cluster as a dictionary.
    """
    with CloudV2() as cloud:
        return cloud.cluster_details(
            cluster_id=cluster_id,
            account=account,
        )


def log_cluster_debug_info(
    cluster_id: int,
    account: str | None = None,
):
    with CloudV2() as cloud:
        details = cloud.cluster_details(cluster_id, account)
        logger.debug("Cluster details:")
        logger.debug(json.dumps(details, indent=2))

        states_by_type = cloud.get_cluster_states(cluster_id, account)

        logger.debug("cluster state history:")
        log_states(flatten_log_states(states_by_type), level=logging.DEBUG)


def create_cluster(
    name: str,
    *,
    software: str | None = None,
    worker_options: dict | None = None,
    scheduler_options: dict | None = None,
    account: str | None = None,
    workers: int = 0,
    environ: dict | None = None,
    tags: dict | None = None,
    dask_config: dict | None = None,
    private_to_creator: bool | None = None,
    scheduler_vm_types: list | None = None,
    worker_vm_types: list | None = None,
    worker_disk_size: int | None = None,
    worker_disk_throughput: int | None = None,
    scheduler_disk_size: int | None = None,
    backend_options: dict | (AWSOptions | GCPOptions) | None = None,
) -> int:
    """Create a cluster

    Parameters
    ---------
    name
        Name of cluster.
    software
        Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".

        The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.
    worker_options
        Mapping with keyword arguments to pass to ``worker_class``. Defaults to ``{}``.
    scheduler_options
        Mapping with keyword arguments to pass to the Scheduler ``__init__``. Defaults to ``{}``.
    account
        Name of the Coiled account to create the cluster in.
        If not provided, will default to ``Cloud.default_account``.
    workers
        Number of workers we to launch.
    environ
        Dictionary of environment variables.
    tags
        Dictionary of instance tags
    dask_config
        Dictionary of dask config to put on cluster

    See Also
    --------
    coiled.Cluster
    """
    with CloudV2(account=account) as cloud:
        cluster, existing = cloud.create_cluster(
            name=name,
            software=software,
            worker_options=worker_options,
            scheduler_options=scheduler_options,
            account=account,
            workers=workers,
            environ=environ,
            tags=tags,
            dask_config=dask_config,
            private_to_creator=private_to_creator,
            backend_options=backend_options,
            worker_vm_types=worker_vm_types,
            worker_disk_size=worker_disk_size,
            worker_disk_throughput=worker_disk_throughput,
            scheduler_disk_size=scheduler_disk_size,
            scheduler_vm_types=scheduler_vm_types,
        )
        return cluster


@list_docstring
def list_clusters(account=None, max_pages: int | None = None):
    with CloudV2() as cloud:
        return cloud.list_clusters(account=account, max_pages=max_pages)


@delete_docstring
def delete_cluster(name: str, account: str | None = None):
    with CloudV2() as cloud:
        cluster_id = cloud.get_cluster_by_name(name=name, account=account)
        if cluster_id is not None:
            return cloud.delete_cluster(cluster_id=cluster_id, account=account)
