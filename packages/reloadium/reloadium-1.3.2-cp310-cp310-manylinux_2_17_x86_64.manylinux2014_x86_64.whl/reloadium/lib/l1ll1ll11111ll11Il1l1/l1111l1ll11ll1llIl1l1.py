import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.l1ll1ll11111ll11Il1l1.l1ll1l1l11ll11l1Il1l1 import lll1l111ll1l1l11Il1l1
from reloadium.lib import l11l1l1l1ll1l111Il1l1

from dataclasses import dataclass

if (TYPE_CHECKING):
    ...


__RELOADIUM__ = True


@dataclass
class llll1lllll1lll1lIl1l1(lll1l111ll1l1l11Il1l1):
    l111l11l111l1111Il1l1 = 'Multiprocessing'

    l1lll11l1111lll1Il1l1 = True

    def __post_init__(llll1l1l1l1l1lllIl1l1) -> None:
        super().__post_init__()

    def l11111l111lll111Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> None:
        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(lll1llllllllll1lIl1l1, 'multiprocessing.popen_spawn_posix')):
            llll1l1l1l1l1lllIl1l1.lll1ll1l111ll1l1Il1l1(lll1llllllllll1lIl1l1)

        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(lll1llllllllll1lIl1l1, 'multiprocessing.popen_spawn_win32')):
            llll1l1l1l1l1lllIl1l1.ll111111l11l1lllIl1l1(lll1llllllllll1lIl1l1)

    def lll1ll1l111ll1l1Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = l11l1l1l1ll1l111Il1l1.l1111l1ll11ll1llIl1l1.l1lll11ll1l11ll1Il1l1  # type: ignore

    def ll111111l11l1lllIl1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = l11l1l1l1ll1l111Il1l1.l1111l1ll11ll1llIl1l1.__init__  # type: ignore
