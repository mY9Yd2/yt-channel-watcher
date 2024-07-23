from dataclasses import dataclass, field
from typing import Any


@dataclass
class SiteData:
    data: dict[str, Any] = field(default_factory=dict)
