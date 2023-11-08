from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.corium.l1l1l1111ll111l1Il1l1 import l1l1l1111ll111l1Il1l1
from reloadium.lib.environ import env
from reloadium.corium.l1l1l1ll111ll11lIl1l1 import llll11l1l11l111lIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l11l11llll11l11lIl1l1 import l11ll111l1ll11l1Il1l1
from reloadium.corium.llll111l1llll1l1Il1l1 import lllllll1llll111lIl1l1, l11l11l1l111111lIl1l1, lllll1111lll111lIl1l1, l11ll1ll11ll1ll1Il1l1
from reloadium.corium.ll111ll1l11l111lIl1l1 import l1ll1ll1ll1lllllIl1l1
from reloadium.corium.l1l1l1ll1ll1l1llIl1l1 import ll1l1l111111ll1lIl1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True

llll1ll1l111ll11Il1l1 = l1l1l1111ll111l1Il1l1.l1111lll11111111Il1l1(__name__)


@dataclass(**l11ll1ll11ll1ll1Il1l1)
class lll11ll1l11l11l1Il1l1(lllll1111lll111lIl1l1):
    l111lllll11l11llIl1l1 = 'FlaskApp'

    @classmethod
    def lll1l1l111l1ll1lIl1l1(l1l1111l11l1llllIl1l1, l111llll11l111llIl1l1: l1ll1ll1ll1lllllIl1l1.ll1l1111l1ll1l1lIl1l1, llll11l111l11111Il1l1: Any, lll1111l111lllllIl1l1: lllllll1llll111lIl1l1) -> bool:
        import flask

        if (isinstance(llll11l111l11111Il1l1, flask.Flask)):
            return True

        return False

    def ll111ll1lll11ll1Il1l1(llll1l1l1l1l1lllIl1l1) -> bool:
        return True

    @classmethod
    def l111111lll1l11llIl1l1(l1l1111l11l1llllIl1l1) -> int:
        return (super().l111111lll1l11llIl1l1() + 10)


@dataclass(**l11ll1ll11ll1ll1Il1l1)
class l1l11llllllll111Il1l1(lllll1111lll111lIl1l1):
    l111lllll11l11llIl1l1 = 'Request'

    @classmethod
    def lll1l1l111l1ll1lIl1l1(l1l1111l11l1llllIl1l1, l111llll11l111llIl1l1: l1ll1ll1ll1lllllIl1l1.ll1l1111l1ll1l1lIl1l1, llll11l111l11111Il1l1: Any, lll1111l111lllllIl1l1: lllllll1llll111lIl1l1) -> bool:
        if (repr(llll11l111l11111Il1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def ll111ll1lll11ll1Il1l1(llll1l1l1l1l1lllIl1l1) -> bool:
        return True

    @classmethod
    def l111111lll1l11llIl1l1(l1l1111l11l1llllIl1l1) -> int:

        return int(10000000000.0)


@dataclass
class ll1l11ll1ll11111Il1l1(l11ll111l1ll11l1Il1l1):
    l111l11l111l1111Il1l1 = 'Flask'

    lll11111l1111l11Il1l1: Any = field(init=False, default=None)
    ll111l1l1l1l11llIl1l1: Any = field(init=False, default=None)
    ll11llll111ll1llIl1l1: Any = field(init=False, default=None)
    ll11ll1111111l1lIl1l1: Any = field(init=False, default=None)

    @contextmanager
    def lllll1ll1l111ll1Il1l1(llll1l1l1l1l1lllIl1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def l11ll11ll1llll11Il1l1(*l111l1l1l11111l1Il1l1: Any, **l1llll1l1l1ll1llIl1l1: Any) -> Any:
            def lll1l1l11lllll11Il1l1(lll1111lll11l1l1Il1l1: Any) -> Any:
                return lll1111lll11l1l1Il1l1

            return lll1l1l11lllll11Il1l1

        l1111l11l11l1111Il1l1 = FlaskLib.route
        FlaskLib.route = l11ll11ll1llll11Il1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = l1111l11l11l1111Il1l1  # type: ignore

    def lll1lll1ll1ll111Il1l1(llll1l1l1l1l1lllIl1l1) -> List[Type[l11l11l1l111111lIl1l1]]:
        return [lll11ll1l11l11l1Il1l1, l1l11llllllll111Il1l1]

    def l11111l111lll111Il1l1(llll1l1l1l1l1lllIl1l1, ll1l11ll1l1l1111Il1l1: types.ModuleType) -> None:
        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(ll1l11ll1l1l1111Il1l1, 'flask.app')):
            llll1l1l1l1l1lllIl1l1.ll111ll11lll111lIl1l1()
            llll1l1l1l1l1lllIl1l1.lllll1l11111lll1Il1l1()
            llll1l1l1l1l1lllIl1l1.l111ll1111l11ll1Il1l1()

        if (llll1l1l1l1l1lllIl1l1.l11l11ll1lll1111Il1l1(ll1l11ll1l1l1111Il1l1, 'flask.cli')):
            llll1l1l1l1l1lllIl1l1.lll1ll1l1ll11lllIl1l1()

    def l1l111l11ll11lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().l1l111l11ll11lllIl1l1()
        try:
            import flask.app  # type: ignore
            import werkzeug.serving  # type: ignore
            import flask.cli  # type: ignore
            flask.app.Flask.dispatch_request = llll1l1l1l1l1lllIl1l1.ll11ll1111111l1lIl1l1
            werkzeug.serving.run_simple = llll1l1l1l1l1lllIl1l1.lll11111l1111l11Il1l1
            flask.cli.run_simple = llll1l1l1l1l1lllIl1l1.lll11111l1111l11Il1l1
            flask.app.Flask.__init__ = llll1l1l1l1l1lllIl1l1.ll111l1l1l1l11llIl1l1
        except ImportError:
            pass

        if (llll1l1l1l1l1lllIl1l1.ll11llll111ll1llIl1l1):
            try:
                import waitress  # type: ignore
                waitress.serve = llll1l1l1l1l1lllIl1l1.ll11llll111ll1llIl1l1
            except ImportError:
                pass

    def ll111ll11lll111lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        llll1l1l1l1l1lllIl1l1.lll11111l1111l11Il1l1 = werkzeug.serving.run_simple

        def l1ll1lll1111l11lIl1l1(*l111l1l1l11111l1Il1l1: Any, **l1llll1l1l1ll1llIl1l1: Any) -> Any:
            with llll11l1l11l111lIl1l1():
                lllllllll1llll1lIl1l1 = l1llll1l1l1ll1llIl1l1.get('port')
                if ( not lllllllll1llll1lIl1l1):
                    lllllllll1llll1lIl1l1 = l111l1l1l11111l1Il1l1[1]

                llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1 = llll1l1l1l1l1lllIl1l1.l11l11111l1lllllIl1l1(lllllllll1llll1lIl1l1)
                if (env.page_reload_on_start):
                    llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l11l1l1ll111l11lIl1l1(1.0)
            llll1l1l1l1l1lllIl1l1.lll11111l1111l11Il1l1(*l111l1l1l11111l1Il1l1, **l1llll1l1l1ll1llIl1l1)

        ll1l1l111111ll1lIl1l1.ll111l11l1l11l1lIl1l1(werkzeug.serving, 'run_simple', l1ll1lll1111l11lIl1l1)
        ll1l1l111111ll1lIl1l1.ll111l11l1l11l1lIl1l1(flask.cli, 'run_simple', l1ll1lll1111l11lIl1l1)

    def l111ll1111l11ll1Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        llll1l1l1l1l1lllIl1l1.ll111l1l1l1l11llIl1l1 = flask.app.Flask.__init__

        def l1ll1lll1111l11lIl1l1(llll111l11l1l111Il1l1: Any, *l111l1l1l11111l1Il1l1: Any, **l1llll1l1l1ll1llIl1l1: Any) -> Any:
            llll1l1l1l1l1lllIl1l1.ll111l1l1l1l11llIl1l1(llll111l11l1l111Il1l1, *l111l1l1l11111l1Il1l1, **l1llll1l1l1ll1llIl1l1)
            with llll11l1l11l111lIl1l1():
                llll111l11l1l111Il1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        ll1l1l111111ll1lIl1l1.ll111l11l1l11l1lIl1l1(flask.app.Flask, '__init__', l1ll1lll1111l11lIl1l1)

    def lllll1l11111lll1Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        llll1l1l1l1l1lllIl1l1.ll11llll111ll1llIl1l1 = waitress.serve


        def l1ll1lll1111l11lIl1l1(*l111l1l1l11111l1Il1l1: Any, **l1llll1l1l1ll1llIl1l1: Any) -> Any:
            with llll11l1l11l111lIl1l1():
                lllllllll1llll1lIl1l1 = l1llll1l1l1ll1llIl1l1.get('port')
                if ( not lllllllll1llll1lIl1l1):
                    lllllllll1llll1lIl1l1 = int(l111l1l1l11111l1Il1l1[1])

                lllllllll1llll1lIl1l1 = int(lllllllll1llll1lIl1l1)

                llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1 = llll1l1l1l1l1lllIl1l1.l11l11111l1lllllIl1l1(lllllllll1llll1lIl1l1)
                if (env.page_reload_on_start):
                    llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l11l1l1ll111l11lIl1l1(1.0)

            llll1l1l1l1l1lllIl1l1.ll11llll111ll1llIl1l1(*l111l1l1l11111l1Il1l1, **l1llll1l1l1ll1llIl1l1)

        ll1l1l111111ll1lIl1l1.ll111l11l1l11l1lIl1l1(waitress, 'serve', l1ll1lll1111l11lIl1l1)

    def lll1ll1l1ll11lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        l111lll111ll1l11Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        l111lll111ll1l11Il1l1 = l111lll111ll1l11Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(l111lll111ll1l11Il1l1, cli.__dict__)

    def l11ll11ll11l1lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().l11ll11ll11l1lllIl1l1()
        import flask.app

        llll1l1l1l1l1lllIl1l1.ll11ll1111111l1lIl1l1 = flask.app.Flask.dispatch_request

        def l1ll1lll1111l11lIl1l1(*l111l1l1l11111l1Il1l1: Any, **l1llll1l1l1ll1llIl1l1: Any) -> Any:
            ll1111l1lll1ll11Il1l1 = llll1l1l1l1l1lllIl1l1.ll11ll1111111l1lIl1l1(*l111l1l1l11111l1Il1l1, **l1llll1l1l1ll1llIl1l1)

            if ( not llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1):
                return ll1111l1lll1ll11Il1l1

            if (isinstance(ll1111l1lll1ll11Il1l1, str)):
                ll1l1l1l1l11l1l1Il1l1 = llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l1111ll1lll1ll11Il1l1(ll1111l1lll1ll11Il1l1)
                return ll1l1l1l1l11l1l1Il1l1
            elif ((isinstance(ll1111l1lll1ll11Il1l1, flask.app.Response) and 'text/html' in ll1111l1lll1ll11Il1l1.content_type)):
                ll1111l1lll1ll11Il1l1.data = llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l1111ll1lll1ll11Il1l1(ll1111l1lll1ll11Il1l1.data.decode('utf-8')).encode('utf-8')
                return ll1111l1lll1ll11Il1l1
            else:
                return ll1111l1lll1ll11Il1l1

        flask.app.Flask.dispatch_request = l1ll1lll1111l11lIl1l1  # type: ignore
