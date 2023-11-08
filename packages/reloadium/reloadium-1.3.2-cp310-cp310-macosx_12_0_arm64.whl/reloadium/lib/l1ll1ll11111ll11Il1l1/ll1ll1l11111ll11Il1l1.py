import sys

from reloadium.corium.l1l1l1ll1ll1l1llIl1l1.lllll111ll1l111lIl1l1 import lll1lll11lll11l1Il1l1

__RELOADIUM__ = True

lll1lll11lll11l1Il1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class ll1l11l1ll1ll111Il1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = ll1l11l1ll1ll111Il1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
