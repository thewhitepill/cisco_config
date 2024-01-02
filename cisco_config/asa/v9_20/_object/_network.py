from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel

from ....command import Argument, Contextual, Positional


__all__ = (
    "Fqdn",
    "Host",
    "NetworkObject"
)


class Fqdn(BaseModel):
    command: Literal["fqdn"]
    value: str


class Host(BaseModel):
    command: Literal["host"]
    value: str


class NetworkObject(BaseModel):
    command: Literal["object"]
    type: Literal["network"]
    name: str
    rename: Annotated[
        Optional[str],
        Argument(
            positional=Positional(explicit=True)
        )
    ]

    target: Annotated[
        Optional[
            Union[
                Fqdn,
                Host
            ]
        ],
        Argument(
            contextual=Contextual(explicit=False),
            positional=Positional(enabled=False)
        )
    ]

    description: Annotated[
        Optional[str],
        Argument(
            varargs=True,
            contextual=Contextual(enabled=True),
            positional=Positional(enabled=False)
        )
    ]
