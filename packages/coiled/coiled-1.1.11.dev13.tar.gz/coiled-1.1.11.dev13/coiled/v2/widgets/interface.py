from __future__ import annotations

from typing import Any, Mapping

from typing_extensions import Protocol


class ClusterWidget(Protocol):
    def update(
        self,
        cluster_details: Mapping[str, Any] | None,
        logs,
        *args,
        final_update=None,
        **kwargs,
    ) -> None:
        pass
