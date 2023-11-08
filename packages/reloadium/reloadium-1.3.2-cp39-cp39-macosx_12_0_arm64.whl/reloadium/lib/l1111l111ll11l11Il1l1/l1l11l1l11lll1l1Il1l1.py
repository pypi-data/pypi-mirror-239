from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import ll1ll1ll1111l11lIl1l1, l1l1l1ll111ll11lIl1l1, public, l11l1ll1ll1ll1llIl1l1, l1l1l1ll1ll1l1llIl1l1
from reloadium.corium.l11l11ll11ll11llIl1l1 import ll1111l1ll111l1lIl1l1, l1l1llllll1ll1llIl1l1
from reloadium.corium.l1l1l1ll111ll11lIl1l1 import lllll111ll111l1lIl1l1, llll11l1l11l111lIl1l1, l11111lll1l111llIl1l1
from reloadium.corium.ll11l11l1llll1l1Il1l1 import ll11lllllllll11lIl1l1
from reloadium.corium.l1l1l1111ll111l1Il1l1 import l1l1l1111ll111l1Il1l1
from reloadium.corium.l1111111ll11l1l1Il1l1 import ll11ll11l1l11111Il1l1
from reloadium.corium.ll1l11111lll1ll1Il1l1 import l1111ll111l11lllIl1l1, l11l11llllll1ll1Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['lll1l11lll111l11Il1l1', 'l1ll1l111l11l1llIl1l1', 'lll111l11l11l111Il1l1']


llll1ll1l111ll11Il1l1 = l1l1l1111ll111l1Il1l1.l1111lll11111111Il1l1(__name__)


class lll1l11lll111l11Il1l1:
    @classmethod
    def l1111l11l11l1lllIl1l1(llll1l1l1l1l1lllIl1l1) -> Optional[FrameType]:
        lll11l1l111llll1Il1l1: FrameType = sys._getframe(2)
        ll1l1l1l1l11l1l1Il1l1 = next(l1l1l1ll1ll1l1llIl1l1.lll11l1l111llll1Il1l1.l1l1lll1l1ll111lIl1l1(lll11l1l111llll1Il1l1))
        return ll1l1l1l1l11l1l1Il1l1


class l1ll1l111l11l1llIl1l1(lll1l11lll111l11Il1l1):
    @classmethod
    def l1111l11l111l111Il1l1(l1l1111l11l1llllIl1l1, l111l1l1l11111l1Il1l1: List[Any], l1llll1l1l1ll1llIl1l1: Dict[str, Any], l1ll1l11111llll1Il1l1: List[l1111ll111l11lllIl1l1]) -> Any:  # type: ignore
        with llll11l1l11l111lIl1l1():
            assert ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1111l111ll11l11Il1l1
            lll11l1l111llll1Il1l1 = ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1111l111ll11l11Il1l1.l1llllllll1ll11lIl1l1.l11l1l1111lll11lIl1l1()
            lll11l1l111llll1Il1l1.lll1111ll1l1ll1lIl1l1()

            l111111llll111l1Il1l1 = ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.ll11111llllll1l1Il1l1.lll1lllll11lll1lIl1l1(lll11l1l111llll1Il1l1.l1111l1l1l1111llIl1l1, lll11l1l111llll1Il1l1.l1ll1ll1lll11lllIl1l1.l1l1ll1ll11ll111Il1l1())
            assert l111111llll111l1Il1l1
            l11l1l1111llllllIl1l1 = l1l1111l11l1llllIl1l1.l1111l11l11l1lllIl1l1()

            for ll1llllll11ll1llIl1l1 in l1ll1l11111llll1Il1l1:
                ll1llllll11ll1llIl1l1.lllll1lll111l11lIl1l1()

            for ll1llllll11ll1llIl1l1 in l1ll1l11111llll1Il1l1:
                ll1llllll11ll1llIl1l1.l1l1l1llll1lll1lIl1l1()


        ll1l1l1l1l11l1l1Il1l1 = l111111llll111l1Il1l1(*l111l1l1l11111l1Il1l1, **l1llll1l1l1ll1llIl1l1);        lll11l1l111llll1Il1l1.l1llll11l11ll1l1Il1l1.additional_info.pydev_step_stop = l11l1l1111llllllIl1l1  # type: ignore

        return ll1l1l1l1l11l1l1Il1l1

    @classmethod
    async def lll1lll11ll11l1lIl1l1(l1l1111l11l1llllIl1l1, l111l1l1l11111l1Il1l1: List[Any], l1llll1l1l1ll1llIl1l1: Dict[str, Any], l1ll1l11111llll1Il1l1: List[l11l11llllll1ll1Il1l1]) -> Any:  # type: ignore
        with llll11l1l11l111lIl1l1():
            assert ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1111l111ll11l11Il1l1
            lll11l1l111llll1Il1l1 = ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1111l111ll11l11Il1l1.l1llllllll1ll11lIl1l1.l11l1l1111lll11lIl1l1()
            lll11l1l111llll1Il1l1.lll1111ll1l1ll1lIl1l1()

            l111111llll111l1Il1l1 = ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.ll11111llllll1l1Il1l1.lll1lllll11lll1lIl1l1(lll11l1l111llll1Il1l1.l1111l1l1l1111llIl1l1, lll11l1l111llll1Il1l1.l1ll1ll1lll11lllIl1l1.l1l1ll1ll11ll111Il1l1())
            assert l111111llll111l1Il1l1
            l11l1l1111llllllIl1l1 = l1l1111l11l1llllIl1l1.l1111l11l11l1lllIl1l1()

            for ll1llllll11ll1llIl1l1 in l1ll1l11111llll1Il1l1:
                await ll1llllll11ll1llIl1l1.lllll1lll111l11lIl1l1()

            for ll1llllll11ll1llIl1l1 in l1ll1l11111llll1Il1l1:
                await ll1llllll11ll1llIl1l1.l1l1l1llll1lll1lIl1l1()


        ll1l1l1l1l11l1l1Il1l1 = await l111111llll111l1Il1l1(*l111l1l1l11111l1Il1l1, **l1llll1l1l1ll1llIl1l1);        lll11l1l111llll1Il1l1.l1llll11l11ll1l1Il1l1.additional_info.pydev_step_stop = l11l1l1111llllllIl1l1  # type: ignore

        return ll1l1l1l1l11l1l1Il1l1


class lll111l11l11l111Il1l1(lll1l11lll111l11Il1l1):
    @classmethod
    def l1111l11l111l111Il1l1(l1l1111l11l1llllIl1l1) -> Optional[ModuleType]:  # type: ignore
        with llll11l1l11l111lIl1l1():
            assert ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1111l111ll11l11Il1l1
            lll11l1l111llll1Il1l1 = ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1111l111ll11l11Il1l1.l1llllllll1ll11lIl1l1.l11l1l1111lll11lIl1l1()

            l11ll11l11llll1lIl1l1 = Path(lll11l1l111llll1Il1l1.llll11l111l11111Il1l1.f_globals['__spec__'].origin).absolute()
            l1ll11l11l1l1lllIl1l1 = lll11l1l111llll1Il1l1.llll11l111l11111Il1l1.f_globals['__name__']
            lll11l1l111llll1Il1l1.lll1111ll1l1ll1lIl1l1()
            l11lll1ll11l1lllIl1l1 = ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l11l11lll111l1llIl1l1.l1lll11l1111l11lIl1l1(l11ll11l11llll1lIl1l1)

            if ( not l11lll1ll11l1lllIl1l1):
                llll1ll1l111ll11Il1l1.llll1ll1l11lll1lIl1l1('Could not retrieve src.', llllll1ll1l11l1lIl1l1={'file': ll11ll11l1l11111Il1l1.ll1ll1111111l1llIl1l1(l11ll11l11llll1lIl1l1), 
'fullname': ll11ll11l1l11111Il1l1.l1ll11l11l1l1lllIl1l1(l1ll11l11l1l1lllIl1l1)})

            assert l11lll1ll11l1lllIl1l1

        try:
            l11lll1ll11l1lllIl1l1.llll11l11ll11111Il1l1()
            l11lll1ll11l1lllIl1l1.l1111lllll111l1lIl1l1(lll11lll1lll1ll1Il1l1=False)
            l11lll1ll11l1lllIl1l1.ll1llll111l1ll11Il1l1(lll11lll1lll1ll1Il1l1=False)
        except lllll111ll111l1lIl1l1 as l1l11ll1111ll11lIl1l1:
            lll11l1l111llll1Il1l1.ll1ll111l1lll111Il1l1(l1l11ll1111ll11lIl1l1)
            return None

        import importlib.util

        ll11l1111l1111llIl1l1 = lll11l1l111llll1Il1l1.llll11l111l11111Il1l1.f_locals['__spec__']
        lll1llllllllll1lIl1l1 = importlib.util.module_from_spec(ll11l1111l1111llIl1l1)

        l11lll1ll11l1lllIl1l1.llll1l11l1l11111Il1l1(lll1llllllllll1lIl1l1)
        return lll1llllllllll1lIl1l1


l1l1llllll1ll1llIl1l1.lll1ll1l1llll11lIl1l1(ll1111l1ll111l1lIl1l1.lll11l1ll1ll11llIl1l1, l1ll1l111l11l1llIl1l1.l1111l11l111l111Il1l1)
l1l1llllll1ll1llIl1l1.lll1ll1l1llll11lIl1l1(ll1111l1ll111l1lIl1l1.l1111ll1lllll111Il1l1, l1ll1l111l11l1llIl1l1.lll1lll11ll11l1lIl1l1)
l1l1llllll1ll1llIl1l1.lll1ll1l1llll11lIl1l1(ll1111l1ll111l1lIl1l1.l111l1l1l11ll11lIl1l1, lll111l11l11l111Il1l1.l1111l11l111l111Il1l1)
