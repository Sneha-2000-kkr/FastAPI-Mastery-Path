from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Item:
    id: int
    name: str
    price_cents: int
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
