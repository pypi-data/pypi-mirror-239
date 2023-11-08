import asyncio
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.ll11l11l1llll1l1Il1l1 import ll11lllllllll11lIl1l1
from reloadium.corium.llll11l11111llllIl1l1 import lll111l1l111ll11Il1l1
from reloadium.lib.environ import env
from reloadium.corium.l1l1l1ll111ll11lIl1l1 import llll11l1l11l111lIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l1ll1l1l11ll11l1Il1l1 import l1ll1l11111l1ll1Il1l1, l11l1l11ll1ll1l1Il1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l11l11llll11l11lIl1l1 import l11ll111l1ll11l1Il1l1
from reloadium.corium.llll111l1llll1l1Il1l1 import l11111lllll1ll1lIl1l1, lllllll1llll111lIl1l1, l11l11l1l111111lIl1l1, lllll1111lll111lIl1l1, l11ll1ll11ll1ll1Il1l1
from reloadium.corium.ll1l11111lll1ll1Il1l1 import l1111ll111l11lllIl1l1, l11l11llllll1ll1Il1l1
from reloadium.corium.ll111ll1l11l111lIl1l1 import l1ll1ll1ll1lllllIl1l1
from reloadium.corium.l1l1l1ll1ll1l1llIl1l1 import ll1l1l111111ll1lIl1l1
from dataclasses import dataclass, field


if (TYPE_CHECKING):
    from django.db import transaction
    from django.db.transaction import Atomic


__RELOADIUM__ = True


@dataclass(**l11ll1ll11ll1ll1Il1l1)
class ll1111l1l1l11111Il1l1(lllll1111lll111lIl1l1):
    l111lllll11l11llIl1l1 = 'Field'

    @classmethod
    def lll1l1l111l1ll1lIl1l1(l1l1111l11l1llllIl1l1, l111llll11l111llIl1l1: l1ll1ll1ll1lllllIl1l1.ll1l1111l1ll1l1lIl1l1, llll11l111l11111Il1l1: Any, lll1111l111lllllIl1l1: lllllll1llll111lIl1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(llll11l111l11111Il1l1, 'field') and isinstance(llll11l111l11111Il1l1.field, Field))):
            return True

        return False

    def lll1l11111lll111Il1l1(llll1l1l1l1l1lllIl1l1, l11lll1ll1l1l1l1Il1l1: l11l11l1l111111lIl1l1) -> bool:
        return True

    @classmethod
    def l111111lll1l11llIl1l1(l1l1111l11l1llllIl1l1) -> int:
        return 200


@dataclass(repr=False)
class lll1ll1ll11ll11lIl1l1(l1ll1l11111l1ll1Il1l1):
    lllll1l11lll1l1lIl1l1: "Atomic" = field(init=False)

    lll111ll1l111ll1Il1l1: bool = field(init=False, default=False)

    def l111lll11lll1111Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().l111lll11lll1111Il1l1()
        from django.db import transaction

        llll1l1l1l1l1lllIl1l1.lllll1l11lll1l1lIl1l1 = transaction.atomic()
        llll1l1l1l1l1lllIl1l1.lllll1l11lll1l1lIl1l1.__enter__()

    def lllll1lll111l11lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().lllll1lll111l11lIl1l1()
        if (llll1l1l1l1l1lllIl1l1.lll111ll1l111ll1Il1l1):
            return 

        llll1l1l1l1l1lllIl1l1.lll111ll1l111ll1Il1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        llll1l1l1l1l1lllIl1l1.lllll1l11lll1l1lIl1l1.__exit__(None, None, None)

    def l1l1l1llll1lll1lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().l1l1l1llll1lll1lIl1l1()

        if (llll1l1l1l1l1lllIl1l1.lll111ll1l111ll1Il1l1):
            return 

        llll1l1l1l1l1lllIl1l1.lll111ll1l111ll1Il1l1 = True
        llll1l1l1l1l1lllIl1l1.lllll1l11lll1l1lIl1l1.__exit__(None, None, None)

    def __repr__(llll1l1l1l1l1lllIl1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class l111ll111l11l1l1Il1l1(l11l1l11ll1ll1l1Il1l1):
    lllll1l11lll1l1lIl1l1: "Atomic" = field(init=False)

    lll111ll1l111ll1Il1l1: bool = field(init=False, default=False)

    async def l111lll11lll1111Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        await super().l111lll11lll1111Il1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        llll1l1l1l1l1lllIl1l1.lllll1l11lll1l1lIl1l1 = transaction.atomic()


        with ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1l11ll111111111Il1l1.lll1lllll11111l1Il1l1(False):
            await sync_to_async(llll1l1l1l1l1lllIl1l1.lllll1l11lll1l1lIl1l1.__enter__)()

    async def lllll1lll111l11lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().lllll1lll111l11lIl1l1()
        if (llll1l1l1l1l1lllIl1l1.lll111ll1l111ll1Il1l1):
            return 

        llll1l1l1l1l1lllIl1l1.lll111ll1l111ll1Il1l1 = True
        from django.db import transaction

        def l1ll11l1l1ll11llIl1l1() -> None:
            transaction.set_rollback(True)
            llll1l1l1l1l1lllIl1l1.lllll1l11lll1l1lIl1l1.__exit__(None, None, None)
        with ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1l11ll111111111Il1l1.lll1lllll11111l1Il1l1(False):
            await sync_to_async(l1ll11l1l1ll11llIl1l1)()

    async def l1l1l1llll1lll1lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().l1l1l1llll1lll1lIl1l1()

        if (llll1l1l1l1l1lllIl1l1.lll111ll1l111ll1Il1l1):
            return 

        llll1l1l1l1l1lllIl1l1.lll111ll1l111ll1Il1l1 = True
        with ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.l1l11ll111111111Il1l1.lll1lllll11111l1Il1l1(False):
            await sync_to_async(llll1l1l1l1l1lllIl1l1.lllll1l11lll1l1lIl1l1.__exit__)(None, None, None)

    def __repr__(llll1l1l1l1l1lllIl1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class l11ll1l1ll11lll1Il1l1(l11ll111l1ll11l1Il1l1):
    l111l11l111l1111Il1l1 = 'Django'

    l1lll1lll1l1llllIl1l1: Optional[int] = field(init=False)
    l11ll1111l11lll1Il1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    l11l1ll1llll111lIl1l1: Any = field(init=False, default=None)
    l11l1lll1ll1l1l1Il1l1: Any = field(init=False, default=None)
    ll1l11lllll1llllIl1l1: Any = field(init=False, default=None)

    l1lll11l1111lll1Il1l1 = True

    def __post_init__(llll1l1l1l1l1lllIl1l1) -> None:
        super().__post_init__()
        llll1l1l1l1l1lllIl1l1.l1lll1lll1l1llllIl1l1 = None

    def lll1lll1ll1ll111Il1l1(llll1l1l1l1l1lllIl1l1) -> List[Type[l11l11l1l111111lIl1l1]]:
        return [ll1111l1l1l11111Il1l1]

    def ll1lllll111ll1l1Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().ll1lllll111ll1l1Il1l1()
        if ('runserver' in sys.argv):
            sys.argv.append('--noreload')

    def l11111l111lll111Il1l1(llll1l1l1l1l1lllIl1l1, lll1llllllllll1lIl1l1: types.ModuleType) -> None:
        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(lll1llllllllll1lIl1l1, 'django.core.management.commands.runserver')):
            llll1l1l1l1l1lllIl1l1.lll1l11l1llll11lIl1l1()
            if ( not llll1l1l1l1l1lllIl1l1.l1l1l11l11ll11llIl1l1):
                llll1l1l1l1l1lllIl1l1.l11l11lll111111lIl1l1()

    def l1l111l11ll11lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        import django.core.management.commands.runserver

        django.core.management.commands.runserver.Command.handle = llll1l1l1l1l1lllIl1l1.l11l1ll1llll111lIl1l1
        django.core.management.commands.runserver.Command.get_handler = llll1l1l1l1l1lllIl1l1.ll1l11lllll1llllIl1l1
        django.core.handlers.base.BaseHandler.get_response = llll1l1l1l1l1lllIl1l1.l11l1lll1ll1l1l1Il1l1

    def l11ll1111lllll11Il1l1(llll1l1l1l1l1lllIl1l1, l111ll1llll11l11Il1l1: str, l1ll1l1llllll111Il1l1: bool) -> Optional["l1111ll111l11lllIl1l1"]:
        if (llll1l1l1l1l1lllIl1l1.l1l1l11l11ll11llIl1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        if (l1ll1l1llllll111Il1l1):
            return None
        else:
            ll1l1l1l1l11l1l1Il1l1 = lll1ll1ll11ll11lIl1l1(l111ll1llll11l11Il1l1=l111ll1llll11l11Il1l1, l1ll1l1l11ll11l1Il1l1=llll1l1l1l1l1lllIl1l1)
            ll1l1l1l1l11l1l1Il1l1.l111lll11lll1111Il1l1()

        return ll1l1l1l1l11l1l1Il1l1

    async def lll11lll1l1l1l11Il1l1(llll1l1l1l1l1lllIl1l1, l111ll1llll11l11Il1l1: str) -> Optional["l11l11llllll1ll1Il1l1"]:
        if (llll1l1l1l1l1lllIl1l1.l1l1l11l11ll11llIl1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        ll1l1l1l1l11l1l1Il1l1 = l111ll111l11l1l1Il1l1(l111ll1llll11l11Il1l1=l111ll1llll11l11Il1l1, l1ll1l1l11ll11l1Il1l1=llll1l1l1l1l1lllIl1l1)
        await ll1l1l1l1l11l1l1Il1l1.l111lll11lll1111Il1l1()
        return ll1l1l1l1l11l1l1Il1l1

    def lll1l11l1llll11lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        import django.core.management.commands.runserver

        llll1l1l1l1l1lllIl1l1.l11l1ll1llll111lIl1l1 = django.core.management.commands.runserver.Command.handle

        def l1ll1lll1111l11lIl1l1(*l111l1l1l11111l1Il1l1: Any, **ll1ll1111l111ll1Il1l1: Any) -> Any:
            with llll11l1l11l111lIl1l1():
                lllllllll1llll1lIl1l1 = ll1ll1111l111ll1Il1l1.get('addrport')
                if ( not lllllllll1llll1lIl1l1):
                    lllllllll1llll1lIl1l1 = django.core.management.commands.runserver.Command.default_port

                lllllllll1llll1lIl1l1 = lllllllll1llll1lIl1l1.split(':')[ - 1]
                lllllllll1llll1lIl1l1 = int(lllllllll1llll1lIl1l1)
                llll1l1l1l1l1lllIl1l1.l1lll1lll1l1llllIl1l1 = lllllllll1llll1lIl1l1

            return llll1l1l1l1l1lllIl1l1.l11l1ll1llll111lIl1l1(*l111l1l1l11111l1Il1l1, **ll1ll1111l111ll1Il1l1)

        ll1l1l111111ll1lIl1l1.ll111l11l1l11l1lIl1l1(django.core.management.commands.runserver.Command, 'handle', l1ll1lll1111l11lIl1l1)

    def l11l11lll111111lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        import django.core.management.commands.runserver

        llll1l1l1l1l1lllIl1l1.ll1l11lllll1llllIl1l1 = django.core.management.commands.runserver.Command.get_handler

        def l1ll1lll1111l11lIl1l1(*l111l1l1l11111l1Il1l1: Any, **ll1ll1111l111ll1Il1l1: Any) -> Any:
            with llll11l1l11l111lIl1l1():
                assert llll1l1l1l1l1lllIl1l1.l1lll1lll1l1llllIl1l1
                llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1 = llll1l1l1l1l1lllIl1l1.l11l11111l1lllllIl1l1(llll1l1l1l1l1lllIl1l1.l1lll1lll1l1llllIl1l1)
                if (env.page_reload_on_start):
                    llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l11l1l1ll111l11lIl1l1(2.0)

            return llll1l1l1l1l1lllIl1l1.ll1l11lllll1llllIl1l1(*l111l1l1l11111l1Il1l1, **ll1ll1111l111ll1Il1l1)

        ll1l1l111111ll1lIl1l1.ll111l11l1l11l1lIl1l1(django.core.management.commands.runserver.Command, 'get_handler', l1ll1lll1111l11lIl1l1)

    def l11ll11ll11l1lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().l11ll11ll11l1lllIl1l1()

        import django.core.handlers.base

        llll1l1l1l1l1lllIl1l1.l11l1lll1ll1l1l1Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def l1ll1lll1111l11lIl1l1(l1111ll1l1llll11Il1l1: Any, l1ll1l111111ll1lIl1l1: Any) -> Any:
            ll1111l1lll1ll11Il1l1 = llll1l1l1l1l1lllIl1l1.l11l1lll1ll1l1l1Il1l1(l1111ll1l1llll11Il1l1, l1ll1l111111ll1lIl1l1)

            if ( not llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1):
                return ll1111l1lll1ll11Il1l1

            ll111l1l11llll1lIl1l1 = ll1111l1lll1ll11Il1l1.get('content-type')

            if (( not ll111l1l11llll1lIl1l1 or 'text/html' not in ll111l1l11llll1lIl1l1)):
                return ll1111l1lll1ll11Il1l1

            lll1l1111ll11l11Il1l1 = ll1111l1lll1ll11Il1l1.content

            if (isinstance(lll1l1111ll11l11Il1l1, bytes)):
                lll1l1111ll11l11Il1l1 = lll1l1111ll11l11Il1l1.decode('utf-8')

            l1111111l1ll1ll1Il1l1 = llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l1111ll1lll1ll11Il1l1(lll1l1111ll11l11Il1l1)

            ll1111l1lll1ll11Il1l1.content = l1111111l1ll1ll1Il1l1.encode('utf-8')
            ll1111l1lll1ll11Il1l1['content-length'] = str(len(ll1111l1lll1ll11Il1l1.content)).encode('ascii')
            return ll1111l1lll1ll11Il1l1

        django.core.handlers.base.BaseHandler.get_response = l1ll1lll1111l11lIl1l1  # type: ignore

    def l1ll111lll1111llIl1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path) -> None:
        super().l1ll111lll1111llIl1l1(ll1ll1111111l1llIl1l1)

        from django.apps.registry import Apps

        llll1l1l1l1l1lllIl1l1.l11ll1111l11lll1Il1l1 = Apps.register_model

        def ll11ll1l111l1111Il1l1(*l111l1l1l11111l1Il1l1: Any, **l1llll1l1l1ll1llIl1l1: Any) -> Any:
            pass

        Apps.register_model = ll11ll1l111l1111Il1l1

    def l1l11ll1l1l1ll11Il1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path, lll11ll11ll11lllIl1l1: List[l11111lllll1ll1lIl1l1]) -> None:
        super().l1l11ll1l1l1ll11Il1l1(ll1ll1111111l1llIl1l1, lll11ll11ll11lllIl1l1)

        if ( not llll1l1l1l1l1lllIl1l1.l11ll1111l11lll1Il1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = llll1l1l1l1l1lllIl1l1.l11ll1111l11lll1Il1l1
