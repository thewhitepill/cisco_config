from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field


__all__ = (
    "Argument",
    "Contextual",
    "Positional"
)


class Contextual(BaseModel):
    enabled: Annotated[bool, Field(default=True)]
    explicit: Annotated[bool, Field(default=True)]


def _default_contextual() -> Contextual:
    return Contextual(enabled=False)


class Positional(BaseModel):
    enabled: Annotated[bool, Field(default=True)]
    explicit: Annotated[bool, Field(default=False)]


class Argument(BaseModel):
    varargs: Annotated[bool, Field(default=False)]

    contextual: Annotated[
        Contextual,
        Field(default_factory=_default_contextual)
    ]

    positional: Annotated[
        Positional,
        Field(default_factory=Positional)
    ]
