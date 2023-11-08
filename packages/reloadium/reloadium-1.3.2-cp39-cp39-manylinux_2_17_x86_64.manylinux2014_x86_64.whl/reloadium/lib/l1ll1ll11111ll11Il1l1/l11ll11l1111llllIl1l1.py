from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.l1ll1ll11111ll11Il1l1.l1ll1l1l11ll11l1Il1l1 import lll1l111ll1l1l11Il1l1
from reloadium.corium.llll111l1llll1l1Il1l1 import l11111lllll1ll1lIl1l1
from reloadium.corium.l1l1l1ll1ll1l1llIl1l1 import ll1l1l111111ll1lIl1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class l1ll11l11lll111lIl1l1(lll1l111ll1l1l11Il1l1):
    l111l11l111l1111Il1l1 = 'PyGame'

    l1lll11l1111lll1Il1l1 = True

    l1111l111lll1l11Il1l1: bool = field(init=False, default=False)

    def l11111l111lll111Il1l1(llll1l1l1l1l1lllIl1l1, ll1l11ll1l1l1111Il1l1: types.ModuleType) -> None:
        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(ll1l11ll1l1l1111Il1l1, 'pygame.base')):
            llll1l1l1l1l1lllIl1l1.l1111llllll1lll1Il1l1()

    def l1111llllll1lll1Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        import pygame.display

        ll1ll11l1lll1l1lIl1l1 = pygame.display.update

        def l1ll1l1lll1l1ll1Il1l1(*l111l1l1l11111l1Il1l1: Any, **l1llll1l1l1ll1llIl1l1: Any) -> None:
            if (llll1l1l1l1l1lllIl1l1.l1111l111lll1l11Il1l1):
                ll1l1l111111ll1lIl1l1.l1l1l1ll11l1ll11Il1l1(0.1)
                return None
            else:
                return ll1ll11l1lll1l1lIl1l1(*l111l1l1l11111l1Il1l1, **l1llll1l1l1ll1llIl1l1)

        pygame.display.update = l1ll1l1lll1l1ll1Il1l1

    def l1ll111lll1111llIl1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path) -> None:
        llll1l1l1l1l1lllIl1l1.l1111l111lll1l11Il1l1 = True

    def l1l11ll1l1l1ll11Il1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path, lll11ll11ll11lllIl1l1: List[l11111lllll1ll1lIl1l1]) -> None:
        llll1l1l1l1l1lllIl1l1.l1111l111lll1l11Il1l1 = False

    def lll1lll11l1l1lllIl1l1(llll1l1l1l1l1lllIl1l1, l111ll11l1111l1lIl1l1: Exception) -> None:
        llll1l1l1l1l1lllIl1l1.l1111l111lll1l11Il1l1 = False
