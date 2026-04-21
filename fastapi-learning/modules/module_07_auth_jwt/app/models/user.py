from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    email: str
    password_hash: str
    roles: list[str] = field(default_factory=lambda: ["user"])
    is_active: bool = True
