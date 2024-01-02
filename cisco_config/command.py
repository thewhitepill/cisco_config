from __future__ import annotations

from typing import (
    Annotated,
    get_origin as get_annotation_origin,
    get_args as get_annotation_args
)

from pydantic import BaseModel, Field

from ._match import Matcher, MatchGenerator
from ._type import TypeHint
from ._utility import find


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


def _get_command_argument_metadata(
    hint: TypeHint
) -> tuple[TypeHint, Argument]:
    if not get_annotation_origin(hint) is Annotated:
        return hint, Argument()

    inner, *rest = get_annotation_args(hint)
    options = find(
        lambda x: isinstance(x, Argument),
        rest,
        default=Argument()
    )

    return inner, options


def _get_command_arguments(
    cls: type[BaseModel]
) -> tuple[str, TypeHint, Argument]:
    for name, hint in cls.__annotations__.items():
        yield (name, *_get_command_argument_metadata(hint))


def _get_matcher_for(hint: TypeHint) -> Matcher:
    pass


class CommandMatcher(Matcher):
    def __init__(self, value: type[BaseModel]) -> None:
        self._value = value

    def match(
        self,
        arguments: list[str]
    ) -> MatchGenerator[tuple[BaseModel, str], None, None]:
        pass
