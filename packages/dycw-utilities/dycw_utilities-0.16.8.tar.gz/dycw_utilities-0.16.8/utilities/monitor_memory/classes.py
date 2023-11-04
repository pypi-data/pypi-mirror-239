from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from typed_settings import option, settings

from utilities.platform import SYSTEM, System
from utilities.typing import never


@settings(frozen=True)
class Config:
    """Settings for the `monitor_memory` script."""

    path: Path = option(
        default=Path("memory.csv"), click={"param_decls": ("-p", "--path")}
    )
    freq: int = option(
        default=60, help="in seconds", click={"param_decls": ("-f", "--freq")}
    )
    duration: Optional[int] = option(  # noqa: UP007
        default=None,
        help="in seconds",
        click={"param_decls": ("-d", "--duration")},
    )


@dataclass(frozen=True)
class ItemWindows:
    """A set of memory statistics."""

    datetime: dt.datetime
    virtual_total: int
    virtual_available: int
    virtual_percent: float
    virtual_used: int
    virtual_free: int
    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float
    swap_sin: int
    swap_sout: int


@dataclass(frozen=True)
class ItemMacOS:
    """A set of memory statistics."""

    datetime: dt.datetime
    virtual_total: int
    virtual_available: int
    virtual_percent: float
    virtual_used: int
    virtual_free: int
    virtual_active: int
    virtual_inactive: int
    virtual_wired: int
    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float
    swap_sin: int
    swap_sout: int


@dataclass(frozen=True)
class ItemLinux:
    """A set of memory statistics."""

    datetime: dt.datetime
    virtual_total: int
    virtual_available: int
    virtual_percent: float
    virtual_used: int
    virtual_free: int
    virtual_active: int
    virtual_inactive: int
    virtual_buffers: int
    virtual_cached: int
    virtual_shared: int
    virtual_slab: int
    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float
    swap_sin: int
    swap_sout: int


if SYSTEM is System.windows:  # pragma: os-ne-windows
    Item = ItemWindows
elif SYSTEM is System.mac:  # pragma: os-ne-macos
    Item = ItemMacOS
elif SYSTEM is System.linux:  # pragma: os-ne-linux
    Item = ItemLinux
else:  # pragma: no cover
    never(SYSTEM)
