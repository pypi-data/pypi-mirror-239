from __future__ import annotations

import re
from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import BinaryIO

from typing_extensions import Literal, TypedDict

logger = getLogger("coiled.package_sync")


event_type_list = Literal[
    "add_role_to_profile",
    "attach_gateway_to_router",
    "attach_subnet_to_router",
    "create_vm",
    "create_machine_image",
    "create_scheduler" "create_worker",
    "delete_machine_image",
    "create_fw_rule",
    "create_fw",
    "create_network_cidr",
    "create_subnet",
    "create_network",
    "create_log_sink",
    "create_router",
    "create_iam_role",
    "create_log_bucket",
    "create_storage_bucket",
    "create_instance_profile",
    "check_log_sink_exists",
    "check_or_attach_cloudwatch_policy",
    "delete_vm",
    "delete_route",
    "get_firewall",
    "get_network",
    "get_subnet",
    "get_policy_arn",
    "get_log_group",
    "gcp_instance_create",
    "net_gateways_get_or_create",
    "scale",
]


class CondaPlaceHolder(dict):
    pass


class PackageInfo(TypedDict):
    name: str
    path: Path | None
    source: Literal["pip", "conda"]
    channel_url: str | None
    channel: str | None
    subdir: str | None
    conda_name: str | None
    version: str
    wheel_target: str | None


class PackageSchema(TypedDict):
    name: str
    source: Literal["pip", "conda"]
    channel: str | None
    conda_name: str | None
    client_version: str | None
    specifier: str
    include: bool
    file: int | None


class ResolvedPackageInfo(TypedDict):
    name: str
    source: Literal["pip", "conda"]
    channel: str | None
    conda_name: str | None
    client_version: str | None
    specifier: str
    include: bool
    note: str | None
    error: str | None
    sdist: BinaryIO | None
    md5: str | None


class PackageLevelEnum(int, Enum):
    """
    Package mismatch severity level
    Using a high int so we have room to add extra levels as needed

    Ordering is allow comparison like

    if somelevel >= PackageLevelEnum.STRICT_MATCH:
        <some logic for high or critical levels>
    """

    CRITICAL = 100
    STRICT_MATCH = 75
    WARN = 50
    NONE = 0
    LOOSE = -1
    IGNORE = -2


class ApproximatePackageRequest(TypedDict):
    name: str
    priority_override: PackageLevelEnum | None
    python_major_version: str
    python_minor_version: str
    python_patch_version: str
    source: Literal["pip", "conda"]
    channel_url: str | None
    channel: str | None
    subdir: str | None
    conda_name: str | None
    version: str
    wheel_target: str | None


class ApproximatePackageResult(TypedDict):
    name: str
    conda_name: str | None
    specifier: str | None
    include: bool
    note: str | None
    error: str | None


class PiplessCondaEnvSchema(TypedDict, total=False):
    name: str | None
    channels: list[str]
    dependencies: list[str]


class CondaEnvSchema(TypedDict, total=False):
    name: str | None
    channels: list[str]
    dependencies: list[str | dict[str, list[str]]]


class SoftwareEnvSpec(TypedDict):
    packages: list[PackageSchema]
    raw_pip: list[str] | None
    raw_conda: CondaEnvSchema | None


class CondaPackage:
    def __init__(self, meta_json: dict, prefix: Path):
        self.prefix = prefix
        self.name: str = meta_json["name"]
        self.version: str = meta_json["version"]
        self.subdir: str = meta_json["subdir"]
        self.files: str = meta_json["files"]
        self.depends: list[str] = meta_json.get("depends", [])
        self.constrains: list[str] = meta_json.get("constrains", [])
        if meta_json["channel"] == "<unknown>":
            logger.warning(f"Channel for {self.name} is unknown, setting to conda-forge")
            meta_json["channel"] = "conda-forge"
        channel_regex = rf"(.*\.\w*)/?(.*)/{self.subdir}$"
        result = re.match(channel_regex, meta_json["channel"])
        if not result:
            self.channel_url = f"https://conda.anaconda.org/{meta_json['channel']}"
            self.channel: str = meta_json["channel"]
        else:
            self.channel_url = result.group(1) + "/" + result.group(2)
            self.channel: str = result.group(2)

    def __repr__(self):
        return (
            f"CondaPackage(meta_json={{'name': {self.name!r}, 'version': "
            f"{self.version!r}, 'subdir': {self.subdir!r}, 'files': {self.files!r}, "
            f"'depends': {self.depends!r}, 'constrains': {self.constrains!r}, "
            f"'channel': {self.channel!r}}}, prefix={self.prefix!r})"
        )

    def __str__(self):
        return f"{self.name} {self.version} from {self.channel_url}"


class PackageLevel(TypedDict):
    name: str
    level: PackageLevelEnum
    source: Literal["pip", "conda"]


class ApiBase(TypedDict):
    id: int
    created: str
    updated: str


class SoftwareEnvironmentBuild(ApiBase):
    state: Literal["built", "building", "error", "queued"]


class SoftwareEnvironmentSpec(ApiBase):
    latest_build: SoftwareEnvironmentBuild | None


class SoftwareEnvironmentAlias(ApiBase):
    name: str
    latest_spec: SoftwareEnvironmentSpec | None


class ArchitectureTypesEnum(str, Enum):
    """
    All currently supported architecture types
    """

    X86_64 = "x86_64"
    ARM64 = "aarch64"

    def __str__(self) -> str:
        return self.value

    @property
    def conda_suffix(self) -> str:
        if self == ArchitectureTypesEnum.X86_64:
            return "64"
        else:
            return self.value

    @property
    def vm_arch(self) -> Literal["x86_64", "arm64"]:
        if self == ArchitectureTypesEnum.ARM64:
            return "arm64"
        else:
            return self.value


class ClusterDetailsState(TypedDict):
    state: str
    reason: str
    updated: str


class ClusterDetailsProcess(TypedDict):
    created: str
    name: str
    current_state: ClusterDetailsState
    instance: dict


class ClusterDetails(TypedDict):
    id: int
    name: str
    workers: list[ClusterDetailsProcess]
    scheduler: ClusterDetailsProcess | None
    current_state: ClusterDetailsState
    created: str


class FirewallOptions(TypedDict):
    """
    A dictionary with the following key/value pairs

    Parameters
    ----------
    ports
        List of ports to open to cidr on the scheduler.
        For example, ``[22, 8786]`` opens port 22 for SSH and 8786 for client to Dask connection.
    cidr
        CIDR block from which to allow access. For example ``0.0.0.0/0`` allows access from any IP address.
    """

    ports: list[int]
    cidr: str


class BackendOptions(TypedDict, total=False):
    """
    A dictionary with the following key/value pairs

    Parameters
    ----------
    region_name
        Region name to launch cluster in. For example: us-east-2
    zone_name
        Zone name to launch cluster in. For example: us-east-2a
    firewall
        Deprecated; use ``ingress`` instead.
    ingress
        Allows you to specify multiple CIDR blocks (and corresponding ports) to open for ingress
        on the scheduler firewall.
    spot
        Whether to request spot instances.
    spot_on_demand_fallback
        If requesting spot, whether to request non-spot instances if we get fewer spot instances
        than desired.
    spot_replacement
        By default we'll attempt to replace interrupted spot instances; set to False to disable.
    multizone
        Tell the cloud provider to pick zone with best availability, we'll keep workers all in the
        same zone, scheduler may or may not be in that zone as well.
    use_dashboard_public_ip
        Public IP is used by default, lets you choose to use private IP for dashboard link.
    use_dashboard_https
        When public IP address is used for dashboard, we'll enable HTTPS + auth by default.
        You may want to disable this if using something that needs to connect directly to
        the scheduler dashboard without authentication, such as jupyter dask-labextension.
    network_volumes
        Very experimental option to allow mounting SMB volume on cluster nodes.
    """

    region_name: str | None
    zone_name: str | None
    firewall: FirewallOptions | None  # TODO deprecate, use ingress instead
    ingress: list[FirewallOptions] | None
    spot: bool | None
    spot_on_demand_fallback: bool | None
    spot_replacement: bool | None
    multizone: bool | None
    use_dashboard_public_ip: bool | None
    use_dashboard_https: bool | None
    send_prometheus_metrics: bool | None  # TODO deprecate
    prometheus_write: dict | None  # TODO deprecate
    network_volumes: list[dict] | None


class AWSOptions(BackendOptions, total=False):
    """
    A dictionary with the following key/value pairs plus any pairs in :py:class:`BackendOptions`

    Parameters
    ----------
    keypair_name
        AWS Keypair to assign worker/scheduler instances. This would need to be an existing keypair in your
            account, and needs to be in the same region as your cluster. Note that Coiled can also manage
            adding a unique, ephemeral keypair for SSH access to your cluster;
            see :doc:`ssh` for more information.
    use_placement_group
        If possible, this will attempt to put workers in the same cluster placement group (in theory this can
        result in better network between workers, since they'd be physically close to each other in datacenter,
        though we haven't seen this to have much benefit in practice).
    """

    keypair_name: str | None
    use_placement_group: bool | None


class GCPOptions(BackendOptions, total=False):
    """
    A dictionary with GCP specific key/value pairs plus any pairs in :py:class:`BackendOptions`
    """

    scheduler_accelerator_count: int | None
    scheduler_accelerator_type: str | None
    worker_accelerator_count: int | None
    worker_accelerator_type: str | None
