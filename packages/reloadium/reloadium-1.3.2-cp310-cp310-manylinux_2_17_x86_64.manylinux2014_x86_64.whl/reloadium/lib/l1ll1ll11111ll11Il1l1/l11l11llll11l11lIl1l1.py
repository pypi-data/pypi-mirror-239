from reloadium.corium.vendored import logging
from pathlib import Path
from threading import Thread
import time
from typing import TYPE_CHECKING, List, Optional

from reloadium.corium import l1l1l1ll1ll1l1llIl1l1
from reloadium.corium.l1l1l1ll1ll1l1llIl1l1.l1llll11l11ll1l1Il1l1 import l111lll11l11ll1lIl1l1
from reloadium.lib.l1ll1ll11111ll11Il1l1.l1ll1l1l11ll11l1Il1l1 import lll1l111ll1l1l11Il1l1
from reloadium.corium.ll11l11l1llll1l1Il1l1 import ll11lllllllll11lIl1l1
from reloadium.corium.l1l1l1111ll111l1Il1l1 import ll111lllllllll11Il1l1
from reloadium.corium.llll111l1llll1l1Il1l1 import l11111lllll1ll1lIl1l1
from reloadium.corium.l11l1ll1ll1ll1llIl1l1 import l11l1ll1ll1ll1llIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.vendored.websocket_server import WebsocketServer


__RELOADIUM__ = True

__all__ = ['l1l1111l1ll1l11lIl1l1']



ll1l1ll1ll111ll1Il1l1 = '\n<!--{info}-->\n<script type="text/javascript">\n   // <![CDATA[  <-- For SVG support\n     function refreshCSS() {\n        var sheets = [].slice.call(document.getElementsByTagName("link"));\n        var head = document.getElementsByTagName("head")[0];\n        for (var i = 0; i < sheets.length; ++i) {\n           var elem = sheets[i];\n           var parent = elem.parentElement || head;\n           parent.removeChild(elem);\n           var rel = elem.rel;\n           if (elem.href && typeof rel != "string" || rel.length === 0 || rel.toLowerCase() === "stylesheet") {\n              var url = elem.href.replace(/(&|\\?)_cacheOverride=\\d+/, \'\');\n              elem.href = url + (url.indexOf(\'?\') >= 0 ? \'&\' : \'?\') + \'_cacheOverride=\' + (new Date().valueOf());\n           }\n           parent.appendChild(elem);\n        }\n     }\n     let protocol = window.location.protocol === \'http:\' ? \'ws://\' : \'wss://\';\n     let address = protocol + "{address}:{port}";\n     let socket = undefined;\n     let lost_connection = false;\n\n     function connect() {\n        socket = new WebSocket(address);\n         socket.onmessage = function (msg) {\n            if (msg.data === \'reload\') window.location.href = window.location.href;\n            else if (msg.data === \'refreshcss\') refreshCSS();\n         };\n     }\n\n     function checkConnection() {\n        if ( socket.readyState === socket.CLOSED ) {\n            lost_connection = true;\n            connect();\n        }\n     }\n\n     connect();\n     setInterval(checkConnection, 500)\n\n   // ]]>\n</script>\n'














































@dataclass
class l1l1111l1ll1l11lIl1l1:
    l111lll11ll1l11lIl1l1: str
    lllllllll1llll1lIl1l1: int
    llll1ll1l111ll11Il1l1: ll111lllllllll11Il1l1

    ll11ll1ll1ll11l1Il1l1: Optional["WebsocketServer"] = field(init=False, default=None)
    lll11111111l1lllIl1l1: str = field(init=False, default='')

    ll1l1lll1l1l1ll1Il1l1 = 'Reloadium page reloader'

    def ll11l1lll1l11lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        from reloadium.vendored.websocket_server import WebsocketServer

        llll1l1l1l1l1lllIl1l1.llll1ll1l111ll11Il1l1.ll1l1lll1l1l1ll1Il1l1(''.join(['Starting reload websocket server on port ', '{:{}}'.format(llll1l1l1l1l1lllIl1l1.lllllllll1llll1lIl1l1, '')]))

        llll1l1l1l1l1lllIl1l1.ll11ll1ll1ll11l1Il1l1 = WebsocketServer(host=llll1l1l1l1l1lllIl1l1.l111lll11ll1l11lIl1l1, port=llll1l1l1l1l1lllIl1l1.lllllllll1llll1lIl1l1)
        llll1l1l1l1l1lllIl1l1.ll11ll1ll1ll11l1Il1l1.run_forever(threaded=True)

        llll1l1l1l1l1lllIl1l1.lll11111111l1lllIl1l1 = ll1l1ll1ll111ll1Il1l1

        llll1l1l1l1l1lllIl1l1.lll11111111l1lllIl1l1 = llll1l1l1l1l1lllIl1l1.lll11111111l1lllIl1l1.replace('{info}', str(llll1l1l1l1l1lllIl1l1.ll1l1lll1l1l1ll1Il1l1))
        llll1l1l1l1l1lllIl1l1.lll11111111l1lllIl1l1 = llll1l1l1l1l1lllIl1l1.lll11111111l1lllIl1l1.replace('{port}', str(llll1l1l1l1l1lllIl1l1.lllllllll1llll1lIl1l1))
        llll1l1l1l1l1lllIl1l1.lll11111111l1lllIl1l1 = llll1l1l1l1l1lllIl1l1.lll11111111l1lllIl1l1.replace('{address}', llll1l1l1l1l1lllIl1l1.l111lll11ll1l11lIl1l1)

    def l1111ll1lll1ll11Il1l1(llll1l1l1l1l1lllIl1l1, l11l1l11lllll1l1Il1l1: str) -> str:
        l1111l1l1l1l1lllIl1l1 = l11l1l11lllll1l1Il1l1.find('<head>')
        if (l1111l1l1l1l1lllIl1l1 ==  - 1):
            l1111l1l1l1l1lllIl1l1 = 0
        ll1l1l1l1l11l1l1Il1l1 = ((l11l1l11lllll1l1Il1l1[:l1111l1l1l1l1lllIl1l1] + llll1l1l1l1l1lllIl1l1.lll11111111l1lllIl1l1) + l11l1l11lllll1l1Il1l1[l1111l1l1l1l1lllIl1l1:])
        return ll1l1l1l1l11l1l1Il1l1

    def lllllll1ll1lll11Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        try:
            llll1l1l1l1l1lllIl1l1.ll11l1lll1l11lllIl1l1()
        except Exception as l1l11ll1111ll11lIl1l1:
            llll1l1l1l1l1lllIl1l1.llll1ll1l111ll11Il1l1.l1l11l1l1l1l1lllIl1l1('Could not start page reload server', lll1111l11ll1l11Il1l1=True)

    def l1l1ll111llll11lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        if ( not llll1l1l1l1l1lllIl1l1.ll11ll1ll1ll11l1Il1l1):
            return 

        llll1l1l1l1l1lllIl1l1.llll1ll1l111ll11Il1l1.ll1l1lll1l1l1ll1Il1l1('Reloading page')
        llll1l1l1l1l1lllIl1l1.ll11ll1ll1ll11l1Il1l1.send_message_to_all('reload')
        l11l1ll1ll1ll1llIl1l1.ll11ll11l111ll1lIl1l1()

    def l1lllllllll11l1lIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        if ( not llll1l1l1l1l1lllIl1l1.ll11ll1ll1ll11l1Il1l1):
            return 

        llll1l1l1l1l1lllIl1l1.llll1ll1l111ll11Il1l1.ll1l1lll1l1l1ll1Il1l1('Stopping reload server')
        llll1l1l1l1l1lllIl1l1.ll11ll1ll1ll11l1Il1l1.shutdown()

    def l11l1l1ll111l11lIl1l1(llll1l1l1l1l1lllIl1l1, l1lll111l11lll1lIl1l1: float) -> None:
        def lllll1l11111l11lIl1l1() -> None:
            time.sleep(l1lll111l11lll1lIl1l1)
            llll1l1l1l1l1lllIl1l1.l1l1ll111llll11lIl1l1()

        l111lll11l11ll1lIl1l1(l11ll11l11111ll1Il1l1=lllll1l11111l11lIl1l1, l111ll1llll11l11Il1l1='page-reloader').start()


@dataclass
class l11ll111l1ll11l1Il1l1(lll1l111ll1l1l11Il1l1):
    ll1l1ll1ll111ll1Il1l1: Optional[l1l1111l1ll1l11lIl1l1] = field(init=False, default=None)

    l1llll11lllll1l1Il1l1 = '127.0.0.1'
    llll1lll1l1ll11lIl1l1 = 4512

    def ll1lllll111ll1l1Il1l1(llll1l1l1l1l1lllIl1l1) -> None:
        ll11lllllllll11lIl1l1.llll11l1l11l11llIl1l1.llll11lll1l11111Il1l1.lll111llll1l1l11Il1l1('html')

    def l1l11ll1l1l1ll11Il1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path, lll11ll11ll11lllIl1l1: List[l11111lllll1ll1lIl1l1]) -> None:
        if ( not llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1):
            return 

        from reloadium.corium.l1111l111ll11l11Il1l1.llllll1111l1ll11Il1l1 import ll11111lll11l1l1Il1l1

        if ( not any((isinstance(l1ll1l11llllll11Il1l1, ll11111lll11l1l1Il1l1) for l1ll1l11llllll11Il1l1 in lll11ll11ll11lllIl1l1))):
            if (llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1):
                llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l1l1ll111llll11lIl1l1()

    def ll11l1lll11l1lllIl1l1(llll1l1l1l1l1lllIl1l1, ll1ll1111111l1llIl1l1: Path) -> None:
        if ( not llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1):
            return 
        llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l1l1ll111llll11lIl1l1()

    def l11l11111l1lllllIl1l1(llll1l1l1l1l1lllIl1l1, lllllllll1llll1lIl1l1: int) -> l1l1111l1ll1l11lIl1l1:
        while True:
            l1lll1ll11llll11Il1l1 = (lllllllll1llll1lIl1l1 + llll1l1l1l1l1lllIl1l1.llll1lll1l1ll11lIl1l1)
            try:
                ll1l1l1l1l11l1l1Il1l1 = l1l1111l1ll1l11lIl1l1(l111lll11ll1l11lIl1l1=llll1l1l1l1l1lllIl1l1.l1llll11lllll1l1Il1l1, lllllllll1llll1lIl1l1=l1lll1ll11llll11Il1l1, llll1ll1l111ll11Il1l1=llll1l1l1l1l1lllIl1l1.ll11lll111111lllIl1l1)
                ll1l1l1l1l11l1l1Il1l1.lllllll1ll1lll11Il1l1()
                llll1l1l1l1l1lllIl1l1.l11ll11ll11l1lllIl1l1()
                break
            except OSError:
                llll1l1l1l1l1lllIl1l1.ll11lll111111lllIl1l1.ll1l1lll1l1l1ll1Il1l1(''.join(["Couldn't create page reloader on ", '{:{}}'.format(l1lll1ll11llll11Il1l1, ''), ' port']))
                llll1l1l1l1l1lllIl1l1.llll1lll1l1ll11lIl1l1 += 1

        return ll1l1l1l1l11l1l1Il1l1

    def l11ll11ll11l1lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        llll1l1l1l1l1lllIl1l1.ll11lll111111lllIl1l1.ll1l1lll1l1l1ll1Il1l1('Injecting page reloader')

    def l1l111l11ll11lllIl1l1(llll1l1l1l1l1lllIl1l1) -> None:
        super().l1l111l11ll11lllIl1l1()

        if (llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1):
            llll1l1l1l1l1lllIl1l1.ll1l1ll1ll111ll1Il1l1.l1lllllllll11l1lIl1l1()
