# Copyright (c) 2017-2023 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# fmt: off
# isort: skip_file

import builtins as _builtins, sys, typing as _typing

from google.protobuf.message import Message as _Message

__all__ = [
    "LedgerOffset",
]


class LedgerOffset(_Message):
    absolute: _builtins.str
    boundary: _typing.Literal[0, 1]
    @_typing.overload
    def __init__(self): ...
    @_typing.overload
    def __init__(self, *, absolute: _builtins.str = ...): ...
    @_typing.overload
    def __init__(self, *, boundary: _typing.Literal['LEDGER_BEGIN', 0, 'LEDGER_END', 1] = ...): ...
    def HasField(self, field_name: _typing.Literal["value", "absolute", "boundary"]) -> _builtins.bool: ...
    def ClearField(self, field_name: _typing.Literal["value", "absolute", "boundary"]) -> None: ...
    def WhichOneof(self, oneof_group: _typing.Literal["value"]) -> _typing.Literal[None, "absolute", "boundary"]: ...
