import dataclasses
import types
from reloadium.lib.l1ll1ll11111ll11Il1l1.l1ll1l1l11ll11l1Il1l1 import lll1l111ll1l1l11Il1l1
from reloadium.fast.l1ll1ll11111ll11Il1l1.ll1lll1111l1llllIl1l1 import l11l1l1lllll1ll1Il1l1

from dataclasses import dataclass

__RELOADIUM__ = True

import types


@dataclass(repr=False, frozen=False)
class l1111l11ll1l1lllIl1l1(lll1l111ll1l1l11Il1l1):
    l111l11l111l1111Il1l1 = 'Pytest'

    def l11111l111lll111Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> None:
        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(lll1llllllllll1lIl1l1, 'pytest')):
            llll1l1l1l1l1lllIl1l1.l11ll1111ll1l11lIl1l1(lll1llllllllll1lIl1l1)

    def l11ll1111ll1l11lIl1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> None:
        import _pytest.assertion.rewrite
        _pytest.assertion.rewrite.AssertionRewritingHook = l11l1l1lllll1ll1Il1l1  # type: ignore

