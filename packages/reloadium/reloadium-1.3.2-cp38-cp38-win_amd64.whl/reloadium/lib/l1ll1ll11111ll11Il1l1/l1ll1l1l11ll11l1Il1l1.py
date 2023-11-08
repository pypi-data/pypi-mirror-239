from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.llll11l11111llllIl1l1 import l111111l1111ll11Il1l1, lll111l1l111ll11Il1l1
from reloadium.corium.l1l1l1111ll111l1Il1l1 import ll111lllllllll11Il1l1, l1l1l1111ll111l1Il1l1
from reloadium.corium.llll111l1llll1l1Il1l1 import l11111lllll1ll1lIl1l1, l11l11l1l111111lIl1l1
from reloadium.corium.ll1l11111lll1ll1Il1l1 import l1111ll111l11lllIl1l1, l11l11llllll1ll1Il1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.lib.l1ll1ll11111ll11Il1l1.l1l1l1l11l1l11llIl1l1 import l1ll1l1l1l1ll11lIl1l1


__RELOADIUM__ = True

llll1ll1l111ll11Il1l1 = l1l1l1111ll111l1Il1l1.l1111lll11111111Il1l1(__name__)


@dataclass
class lll1l111ll1l1l11Il1l1:
    l1l1l1l11l1l11llIl1l1: "l1ll1l1l1l1ll11lIl1l1"
    llll11l11111llllIl1l1: l111111l1111ll11Il1l1

    l111l11l111l1111Il1l1: ClassVar[str] = NotImplemented
    l1111lllll1ll11lIl1l1: bool = field(init=False, default=False)

    ll11lll111111lllIl1l1: ll111lllllllll11Il1l1 = field(init=False)

    l1l1l11l11ll11llIl1l1: bool = field(init=False, default=False)

    l1lll11l1111lll1Il1l1 = False

    def __post_init__(llll1l1l1l1l1lllIl1l1) -> None:
        llll1l1l1l1l1lllIl1l1.ll11lll111111lllIl1l1 = l1l1l1111ll111l1Il1l1.l1111lll11111111Il1l1(llll1l1l1l1l1lllIl1l1.l111l11l111l1111Il1l1)
        llll1l1l1l1l1lllIl1l1.ll11lll111111lllIl1l1.ll1l1lll1l1l1ll1Il1l1('Creating extension')
        llll1l1l1l1l1lllIl1l1.l1l1l1l11l1l11llIl1l1.llll11l1l11l11llIl1l1.l1ll1l1l11lllll1Il1l1.l1ll1l111111111lIl1l1(llll1l1l1l1l1lllIl1l1.ll111lll1ll1l11lIl1l1())
        llll1l1l1l1l1lllIl1l1.l1l1l11l11ll11llIl1l1 = isinstance(llll1l1l1l1l1lllIl1l1.llll11l11111llllIl1l1, lll111l1l111ll11Il1l1)

    def ll111lll1ll1l11lIl1l1(llll1l1l1l1l1lllIl1l1) -> List[Type[l11l11l1l111111lIl1l1]]:
        ll1l1l1l1l11l1l1Il1l1 = []
        llll111l1llll1l1Il1l1 = llll1l1l1l1l1lllIl1l1.lll1lll1ll1ll111Il1l1()
        for l1ll1l1ll11l1111Il1l1 in llll111l1llll1l1Il1l1:
            l1ll1l1ll11l1111Il1l1.lll111111ll11l11Il1l1 = llll1l1l1l1l1lllIl1l1.l111l11l111l1111Il1l1

        ll1l1l1l1l11l1l1Il1l1.extend(llll111l1llll1l1Il1l1)
        return ll1l1l1l1l11l1l1Il1l1

    def l1lllllllll1llllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        llll1l1l1l1l1lllIl1l1.l1111lllll1ll11lIl1l1 = True

    def l11111l111lll111Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> None:
        pass

    @classmethod
    def llll1l1l1l11ll11Il1l1(l1l1111l11l1llllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> bool:
        if ( not hasattr(lll1llllllllll1lIl1l1, '__name__')):
            return False

        ll1l1l1l1l11l1l1Il1l1 = lll1llllllllll1lIl1l1.__name__.split('.')[0].lower() == l1l1111l11l1llllIl1l1.l111l11l111l1111Il1l1.lower()
        return ll1l1l1l1l11l1l1Il1l1

    def l1l111l11ll11lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        llll1ll1l111ll11Il1l1.ll1l1lll1l1l1ll1Il1l1(''.join(['Disabling extension ', '{:{}}'.format(llll1l1l1l1l1lllIl1l1.l111l11l111l1111Il1l1, '')]))

    @contextmanager
    def lllll1ll1l111ll1Il1l1(llll1l1l1l1l1lllIl1l1) -> Generator[None, None, None]:
        yield 

    def ll1lllll111ll1l1Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        pass

    def lll1lll11l1l1lllIl1l1(llll1l1l1l1l1lllIl1l1, l111ll11l1111l1lIl1l1: Exception) -> None:
        pass

    def l11ll1111lllll11Il1l1(llll1l1l1l1l1lllIl1l1, l111ll1llll11l11Il1l1: str, l1ll1l1llllll111Il1l1: bool) -> Optional[l1111ll111l11lllIl1l1]:
        return None

    async def lll11lll1l1l1l11Il1l1(llll1l1l1l1l1lllIl1l1, l111ll1llll11l11Il1l1: str) -> Optional[l11l11llllll1ll1Il1l1]:
        return None

    def llll1111l111ll1lIl1l1(llll1l1l1l1l1lllIl1l1, l111ll1llll11l11Il1l1: str) -> Optional[l1111ll111l11lllIl1l1]:
        return None

    async def l111l111l1l111llIl1l1(llll1l1l1l1l1lllIl1l1, l111ll1llll11l11Il1l1: str) -> Optional[l11l11llllll1ll1Il1l1]:
        return None

    def ll11l1lll11l1lllIl1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path) -> None:
        pass

    def l1ll111lll1111llIl1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path) -> None:
        pass

    def l1l11ll1l1l1ll11Il1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path, lll11ll11ll11lllIl1l1: List[l11111lllll1ll1lIl1l1]) -> None:
        pass

    def __eq__(llll1l1l1l1l1lllIl1l1, ll1ll11111111ll1Il1l1: Any) -> bool:
        return id(ll1ll11111111ll1Il1l1) == id(llll1l1l1l1l1lllIl1l1)

    def lll1lll1ll1ll111Il1l1(llll1l1l1l1l1lllIl1l1) -> List[Type[l11l11l1l111111lIl1l1]]:
        return []

    def l11l11ll1lll1111Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType, l111ll1llll11l11Il1l1: str) -> bool:
        ll1l1l1l1l11l1l1Il1l1 = (hasattr(lll1llllllllll1lIl1l1, '__name__') and lll1llllllllll1lIl1l1.__name__ == l111ll1llll11l11Il1l1)
        return ll1l1l1l1l11l1l1Il1l1


@dataclass(repr=False)
class l1ll1l11111l1ll1Il1l1(l1111ll111l11lllIl1l1):
    l1ll1l1l11ll11l1Il1l1: lll1l111ll1l1l11Il1l1

    def __repr__(llll1l1l1l1l1lllIl1l1) -> str:
        return 'ExtensionMemento'


@dataclass(repr=False)
class l11l1l11ll1ll1l1Il1l1(l11l11llllll1ll1Il1l1):
    l1ll1l1l11ll11l1Il1l1: lll1l111ll1l1l11Il1l1

    def __repr__(llll1l1l1l1l1lllIl1l1) -> str:
        return 'AsyncExtensionMemento'
