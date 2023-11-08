from dataclasses import dataclass, field
from types import CodeType, ModuleType
from typing import TYPE_CHECKING, Any, Callable, Optional
import inspect

from reloadium.lib.l1ll1ll11111ll11Il1l1.l11l11llll11l11lIl1l1 import l11ll111l1ll11l1Il1l1

if (TYPE_CHECKING):
    pass


__RELOADIUM__ = True


@dataclass
class l1l1l1l1l1ll111lIl1l1(l11ll111l1ll11l1Il1l1):
    l111l11l111l1111Il1l1 = 'Numba'

    l1lll11l1111lll1Il1l1 = True

    def __post_init__(llll1l1l1l1l1lllIl1l1) -> None:
        super().__post_init__()

    def l11111l111lll111Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: ModuleType) -> None:
        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(lll1llllllllll1lIl1l1, 'numba.core.bytecode')):
            llll1l1l1l1l1lllIl1l1.l111l111l11ll1llIl1l1()

    def l111l111l11ll1llIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        import numba.core.bytecode

        def l11l1ll111l1l11lIl1l1(l11ll11l1ll1l1l1Il1l1) -> CodeType:  # type: ignore
            import ast
            ll1l1l1l1l11l1l1Il1l1 = getattr(l11ll11l1ll1l1l1Il1l1, '__code__', getattr(l11ll11l1ll1l1l1Il1l1, 'func_code', None))  # type: ignore

            if ('__rw_mode__' in ll1l1l1l1l11l1l1Il1l1.co_consts):  # type: ignore
                l1ll1lllll1lll11Il1l1 = ast.parse(inspect.getsource(l11ll11l1ll1l1l1Il1l1))
                l11111ll111lllllIl1l1 = l1ll1lllll1lll11Il1l1.body[0]
                l11111ll111lllllIl1l1.decorator_list = []  # type: ignore

                l1111l1l1l1111llIl1l1 = compile(l1ll1lllll1lll11Il1l1, filename=ll1l1l1l1l11l1l1Il1l1.co_filename, mode='exec')  # type: ignore
                ll1l1l1l1l11l1l1Il1l1 = l1111l1l1l1111llIl1l1.co_consts[0]

            return ll1l1l1l1l11l1l1Il1l1  # type: ignore

        numba.core.bytecode.get_code_object.__code__ = l11l1ll111l1l11lIl1l1.__code__
