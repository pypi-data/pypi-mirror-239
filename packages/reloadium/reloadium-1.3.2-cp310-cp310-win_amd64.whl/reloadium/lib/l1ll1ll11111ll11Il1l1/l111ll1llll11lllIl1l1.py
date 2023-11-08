import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.l1l1l1ll111ll11lIl1l1 import llll11l1l11l111lIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l1ll1l1l11ll11l1Il1l1 import lll1l111ll1l1l11Il1l1, l1ll1l11111l1ll1Il1l1
from reloadium.corium.ll1l11111lll1ll1Il1l1 import l1111ll111l11lllIl1l1
from reloadium.corium.l1l1l1ll1ll1l1llIl1l1 import ll1l1l111111ll1lIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session


__RELOADIUM__ = True


@dataclass(repr=False)
class lll1ll1ll11ll11lIl1l1(l1ll1l11111l1ll1Il1l1):
    l1ll1l1l11ll11l1Il1l1: "l111lll11ll111l1Il1l1"
    l1lll1l1111l111lIl1l1: List["Transaction"] = field(init=False, default_factory=list)

    def l111lll11lll1111Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().l111lll11lll1111Il1l1()

        lllllll1111l11l1Il1l1 = list(_sessions.values())

        for l1ll1l11ll1l11llIl1l1 in lllllll1111l11l1Il1l1:
            if ( not l1ll1l11ll1l11llIl1l1.is_active):
                continue

            ll1lll11lll1l1llIl1l1 = l1ll1l11ll1l11llIl1l1.begin_nested()
            llll1l1l1l1l1lllIl1l1.l1lll1l1111l111lIl1l1.append(ll1lll11lll1l1llIl1l1)

    def __repr__(llll1l1l1l1l1lllIl1l1) -> str:
        return 'DbMemento'

    def lllll1lll111l11lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().lllll1lll111l11lIl1l1()

        while llll1l1l1l1l1lllIl1l1.l1lll1l1111l111lIl1l1:
            ll1lll11lll1l1llIl1l1 = llll1l1l1l1l1lllIl1l1.l1lll1l1111l111lIl1l1.pop()
            if (ll1lll11lll1l1llIl1l1.is_active):
                try:
                    ll1lll11lll1l1llIl1l1.rollback()
                except :
                    pass

    def l1l1l1llll1lll1lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().l1l1l1llll1lll1lIl1l1()

        while llll1l1l1l1l1lllIl1l1.l1lll1l1111l111lIl1l1:
            ll1lll11lll1l1llIl1l1 = llll1l1l1l1l1lllIl1l1.l1lll1l1111l111lIl1l1.pop()
            if (ll1lll11lll1l1llIl1l1.is_active):
                try:
                    ll1lll11lll1l1llIl1l1.commit()
                except :
                    pass


@dataclass
class l111lll11ll111l1Il1l1(lll1l111ll1l1l11Il1l1):
    l111l11l111l1111Il1l1 = 'Sqlalchemy'

    ll1ll1l1l1l111l1Il1l1: List["Engine"] = field(init=False, default_factory=list)
    lllllll1111l11l1Il1l1: Set["Session"] = field(init=False, default_factory=set)
    llll111lllll1l11Il1l1: Tuple[int, ...] = field(init=False)

    def l11111l111lll111Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> None:
        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(lll1llllllllll1lIl1l1, 'sqlalchemy')):
            llll1l1l1l1l1lllIl1l1.l11l111l1llll1l1Il1l1(lll1llllllllll1lIl1l1)

        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(lll1llllllllll1lIl1l1, 'sqlalchemy.engine.base')):
            llll1l1l1l1l1lllIl1l1.l111lll1l1l1llllIl1l1(lll1llllllllll1lIl1l1)

    def l11l111l1llll1l1Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: Any) -> None:
        lll1l1111ll11l11Il1l1 = Path(lll1llllllllll1lIl1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', lll1l1111ll11l11Il1l1)[0]

        l1111l1l11l11l1lIl1l1 = [int(ll11ll11ll1ll1llIl1l1) for ll11ll11ll1ll1llIl1l1 in __version__.split('.')]
        llll1l1l1l1l1lllIl1l1.llll111lllll1l11Il1l1 = tuple(l1111l1l11l11l1lIl1l1)

    def l11ll1111lllll11Il1l1(llll1l1l1l1l1lllIl1l1, l111ll1llll11l11Il1l1: str, l1ll1l1llllll111Il1l1: bool) -> Optional["l1111ll111l11lllIl1l1"]:
        ll1l1l1l1l11l1l1Il1l1 = lll1ll1ll11ll11lIl1l1(l111ll1llll11l11Il1l1=l111ll1llll11l11Il1l1, l1ll1l1l11ll11l1Il1l1=llll1l1l1l1l1lllIl1l1)
        ll1l1l1l1l11l1l1Il1l1.l111lll11lll1111Il1l1()
        return ll1l1l1l1l11l1l1Il1l1

    def l111lll1l1l1llllIl1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: Any) -> None:
        llll11l11l111l1lIl1l1 = locals().copy()

        llll11l11l111l1lIl1l1.update({'original': lll1llllllllll1lIl1l1.Engine.__init__, 'reloader_code': llll11l1l11l111lIl1l1, 'engines': llll1l1l1l1l1lllIl1l1.ll1ll1l1l1l111l1Il1l1})





        l11l1l11ll111l11Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        lll1lll11lllll1lIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (llll1l1l1l1l1lllIl1l1.llll111lllll1l11Il1l1 <= (1, 3, 24, )):
            exec(l11l1l11ll111l11Il1l1, {**globals(), **llll11l11l111l1lIl1l1}, llll11l11l111l1lIl1l1)
        else:
            exec(lll1lll11lllll1lIl1l1, {**globals(), **llll11l11l111l1lIl1l1}, llll11l11l111l1lIl1l1)

        ll1l1l111111ll1lIl1l1.ll111l11l1l11l1lIl1l1(lll1llllllllll1lIl1l1.Engine, '__init__', llll11l11l111l1lIl1l1['patched'])
