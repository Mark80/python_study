from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class User: 
    id: int
    name: str
    email: str

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "User":
        return cls(
            id=int(record["id"]),
            name=str(record["name"]),
            email=str(record["email"]),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "User":
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            email=str(data["email"]),
        )       