from contextlib import contextmanager
from pathlib import Path
import sys
import types
from threading import Timer, Thread
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type, Set


import reloadium.lib.l1ll1ll11111ll11Il1l1.ll1ll1l11111ll11Il1l1
from reloadium.corium import l1llllll1ll11ll1Il1l1, ll1ll1ll1111l11lIl1l1, l1l1l1ll1ll1l1llIl1l1
from reloadium.corium.lll1l1l11l111lllIl1l1 import llll111llll1111lIl1l1
from reloadium.corium.llll11l11111llllIl1l1 import l111111l1111ll11Il1l1, ll1lll11ll11111lIl1l1
from reloadium.corium.l1l1l1ll1ll1l1llIl1l1.l1llll11l11ll1l1Il1l1 import l111lll11l11ll1lIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.ll1ll1ll1l111111Il1l1 import l11ll1l1ll11lll1Il1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l1ll1l1l11ll11l1Il1l1 import lll1l111ll1l1l11Il1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.lll1lll11ll11l11Il1l1 import llll11l1llll1lllIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.ll1l1ll1l11lll11Il1l1 import ll1l11ll1ll11111Il1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l1llll1ll11111l1Il1l1 import l11l1l11ll1111llIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.lll1l111l11lll1lIl1l1 import l1l1l1l1l1ll111lIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.llll1ll1ll111l11Il1l1 import l1l1lll1l11l11llIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l11ll11l1111llllIl1l1 import l1ll11l11lll111lIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.ll1lll1111l1llllIl1l1 import l1111l11ll1l1lllIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l111ll1llll11lllIl1l1 import l111lll11ll111l1Il1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l1111l1ll11ll1llIl1l1 import llll1lllll1lll1lIl1l1
from reloadium.corium.l1l1l1111ll111l1Il1l1 import l1l1l1111ll111l1Il1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.corium.llll11l1l11l11llIl1l1 import l1l1llll111lllllIl1l1
    from reloadium.corium.llll111l1llll1l1Il1l1 import l11111lllll1ll1lIl1l1


__RELOADIUM__ = True

llll1ll1l111ll11Il1l1 = l1l1l1111ll111l1Il1l1.l1111lll11111111Il1l1(__name__)


@dataclass
class l1ll1l1l1l1ll11lIl1l1:
    llll11l1l11l11llIl1l1: "l1l1llll111lllllIl1l1"

    l1ll1ll11111ll11Il1l1: List[lll1l111ll1l1l11Il1l1] = field(init=False, default_factory=list)

    l1l11lllll11l1llIl1l1: List[types.ModuleType] = field(init=False, default_factory=list)

    l111lll11lll1ll1Il1l1: List[Type[lll1l111ll1l1l11Il1l1]] = field(init=False, default_factory=lambda :[ll1l11ll1ll11111Il1l1, l1l1lll1l11l11llIl1l1, l11ll1l1ll11lll1Il1l1, l111lll11ll111l1Il1l1, l1ll11l11lll111lIl1l1, l11l1l11ll1111llIl1l1, l1111l11ll1l1lllIl1l1, llll1lllll1lll1lIl1l1, llll11l1llll1lllIl1l1, l1l1l1l1l1ll111lIl1l1])




    l111l11111lllll1Il1l1: List[Type[lll1l111ll1l1l11Il1l1]] = field(init=False, default_factory=list)
    llll1ll1l1ll1l1lIl1l1 = 5

    def __post_init__(llll1l1l1l1l1lllIl1l1) -> None:
        if (llll111llll1111lIl1l1().l1l11llllll11l11Il1l1.ll1l11ll1l1l11llIl1l1):
            llll1l1l1l1l1lllIl1l1.l111lll11lll1ll1Il1l1.remove(l1111l11ll1l1lllIl1l1)

        l111lll11l11ll1lIl1l1(l11ll11l11111ll1Il1l1=llll1l1l1l1l1lllIl1l1.ll1111l11l1111llIl1l1, l111ll1llll11l11Il1l1='show-forbidden-dialog').start()

    def ll1111l11l1111llIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        l1l1l1ll1ll1l1llIl1l1.ll1l1l111111ll1lIl1l1.l1l1l1ll11l1ll11Il1l1(llll1l1l1l1l1lllIl1l1.llll1ll1l1ll1l1lIl1l1)

        llll1l1l1l1l1lllIl1l1.llll11l1l11l11llIl1l1.l11l1llll1l11111Il1l1.l1l11l1l11ll1lllIl1l1()

        if ( not llll1l1l1l1l1lllIl1l1.l111l11111lllll1Il1l1):
            return 

        l1ll1ll11111ll11Il1l1 = [l1l11ll1111ll11lIl1l1.l111l11l111l1111Il1l1 for l1l11ll1111ll11lIl1l1 in llll1l1l1l1l1lllIl1l1.l111l11111lllll1Il1l1]
        llll1l1l1l1l1lllIl1l1.llll11l1l11l11llIl1l1.ll1111ll1l1l11llIl1l1.lllll1lll1l11lllIl1l1(ll1lll11ll11111lIl1l1.l11111ll11llll1lIl1l1, ll1ll1ll1111l11lIl1l1.ll1l11l1lllll11lIl1l1.l1ll1l11lllll1llIl1l1(l1ll1ll11111ll11Il1l1), 
ll11ll111l1l1l1lIl1l1='')

    def l1111ll1ll1111llIl1l1(llll1l1l1l1l1lllIl1l1, l11lll111llllll1Il1l1: types.ModuleType) -> None:
        for l1111l11ll111ll1Il1l1 in llll1l1l1l1l1lllIl1l1.l111lll11lll1ll1Il1l1.copy():
            if (l1111l11ll111ll1Il1l1.llll1l1l1l11ll11Il1l1(l11lll111llllll1Il1l1)):
                if (( not l1111l11ll111ll1Il1l1.l1lll11l1111lll1Il1l1 and llll1l1l1l1l1lllIl1l1.llll11l1l11l11llIl1l1.ll1111ll1l1l11llIl1l1.llll11l11111llllIl1l1.ll1lll11l11111llIl1l1([l1111l11ll111ll1Il1l1.l111l11l111l1111Il1l1]) is False)):
                    llll1l1l1l1l1lllIl1l1.l111l11111lllll1Il1l1.append(l1111l11ll111ll1Il1l1)
                    llll1l1l1l1l1lllIl1l1.l111lll11lll1ll1Il1l1.remove(l1111l11ll111ll1Il1l1)
                    continue
                llll1l1l1l1l1lllIl1l1.lll111ll111l1lllIl1l1(l1111l11ll111ll1Il1l1)

        if (l11lll111llllll1Il1l1 in llll1l1l1l1l1lllIl1l1.l1l11lllll11l1llIl1l1):
            return 

        for ll11ll111ll1111lIl1l1 in llll1l1l1l1l1lllIl1l1.l1ll1ll11111ll11Il1l1.copy():
            ll11ll111ll1111lIl1l1.l11111l111lll111Il1l1(l11lll111llllll1Il1l1)

        llll1l1l1l1l1lllIl1l1.l1l11lllll11l1llIl1l1.append(l11lll111llllll1Il1l1)

    def lll111ll111l1lllIl1l1(llll1l1l1l1l1lllIl1l1, l1111l11ll111ll1Il1l1: Type[lll1l111ll1l1l11Il1l1]) -> None:
        llll11l1l1ll1lllIl1l1 = l1111l11ll111ll1Il1l1(llll1l1l1l1l1lllIl1l1, llll1l1l1l1l1lllIl1l1.llll11l1l11l11llIl1l1.ll1111ll1l1l11llIl1l1.llll11l11111llllIl1l1)

        llll1l1l1l1l1lllIl1l1.llll11l1l11l11llIl1l1.l11l111111ll11llIl1l1.l111ll11l11111llIl1l1.l111l1llll1lllllIl1l1(l1llllll1ll11ll1Il1l1.lll11l111l11l111Il1l1(llll11l1l1ll1lllIl1l1))
        llll11l1l1ll1lllIl1l1.ll1lllll111ll1l1Il1l1()
        llll1l1l1l1l1lllIl1l1.l1ll1ll11111ll11Il1l1.append(llll11l1l1ll1lllIl1l1)

        if (l1111l11ll111ll1Il1l1 in llll1l1l1l1l1lllIl1l1.l111lll11lll1ll1Il1l1):
            llll1l1l1l1l1lllIl1l1.l111lll11lll1ll1Il1l1.remove(l1111l11ll111ll1Il1l1)

    @contextmanager
    def lllll1ll1l111ll1Il1l1(llll1l1l1l1l1lllIl1l1) -> Generator[None, None, None]:
        lllll1111ll1ll1lIl1l1 = [ll11ll111ll1111lIl1l1.lllll1ll1l111ll1Il1l1() for ll11ll111ll1111lIl1l1 in llll1l1l1l1l1lllIl1l1.l1ll1ll11111ll11Il1l1.copy()]

        for ll1111ll1l111111Il1l1 in lllll1111ll1ll1lIl1l1:
            ll1111ll1l111111Il1l1.__enter__()

        yield 

        for ll1111ll1l111111Il1l1 in lllll1111ll1ll1lIl1l1:
            ll1111ll1l111111Il1l1.__exit__(*sys.exc_info())

    def l1ll111lll1111llIl1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path) -> None:
        for ll11ll111ll1111lIl1l1 in llll1l1l1l1l1lllIl1l1.l1ll1ll11111ll11Il1l1.copy():
            ll11ll111ll1111lIl1l1.l1ll111lll1111llIl1l1(ll1ll1111111l1llIl1l1)

    def ll11l1lll11l1lllIl1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path) -> None:
        for ll11ll111ll1111lIl1l1 in llll1l1l1l1l1lllIl1l1.l1ll1ll11111ll11Il1l1.copy():
            ll11ll111ll1111lIl1l1.ll11l1lll11l1lllIl1l1(ll1ll1111111l1llIl1l1)

    def lll1lll11l1l1lllIl1l1(llll1l1l1l1l1lllIl1l1, l111ll11l1111l1lIl1l1: Exception) -> None:
        for ll11ll111ll1111lIl1l1 in llll1l1l1l1l1lllIl1l1.l1ll1ll11111ll11Il1l1.copy():
            ll11ll111ll1111lIl1l1.lll1lll11l1l1lllIl1l1(l111ll11l1111l1lIl1l1)

    def l1l11ll1l1l1ll11Il1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path, lll11ll11ll11lllIl1l1: List["l11111lllll1ll1lIl1l1"]) -> None:
        for ll11ll111ll1111lIl1l1 in llll1l1l1l1l1lllIl1l1.l1ll1ll11111ll11Il1l1.copy():
            ll11ll111ll1111lIl1l1.l1l11ll1l1l1ll11Il1l1(ll1ll1111111l1llIl1l1, lll11ll11ll11lllIl1l1)

    def lll11l1lll11llllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        llll1l1l1l1l1lllIl1l1.l1ll1ll11111ll11Il1l1.clear()
