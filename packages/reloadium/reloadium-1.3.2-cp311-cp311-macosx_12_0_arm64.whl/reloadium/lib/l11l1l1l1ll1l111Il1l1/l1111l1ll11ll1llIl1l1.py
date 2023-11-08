import sys

__RELOADIUM__ = True


def l1lll11ll1l11ll1Il1l1(llll111l11l1l111Il1l1, l11llllll1llllllIl1l1):
    from reloadium.lib.environ import env
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    env.sub_process += 1
    env.save_to_os_environ()

    def l1ll11l1ll1lll1lIl1l1(*ll1ll111l1l1ll1lIl1l1):

        for ll1ll11lllllllllIl1l1 in ll1ll111l1l1ll1lIl1l1:
            os.close(ll1ll11lllllllllIl1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    l111l11l1ll11lllIl1l1 = tracker.getfd()
    llll111l11l1l111Il1l1._fds.append(l111l11l1ll11lllIl1l1)
    l1l1ll1111l1lll1Il1l1 = spawn.get_preparation_data(l11llllll1llllllIl1l1._name)
    llll1lll11l11ll1Il1l1 = io.BytesIO()
    set_spawning_popen(llll111l11l1l111Il1l1)

    try:
        reduction.dump(l1l1ll1111l1lll1Il1l1, llll1lll11l11ll1Il1l1)
        reduction.dump(l11llllll1llllllIl1l1, llll1lll11l11ll1Il1l1)
    finally:
        set_spawning_popen(None)

    lll1lll1ll111lllIl1l1l111ll1ll1l1ll1lIl1l1lll111l111111l11Il1l1ll1111ll1l111l11Il1l1 = None
    try:
        (lll1lll1ll111lllIl1l1, l111ll1ll1l1ll1lIl1l1, ) = os.pipe()
        (lll111l111111l11Il1l1, ll1111ll1l111l11Il1l1, ) = os.pipe()
        l1llll1ll111l1l1Il1l1 = spawn.get_command_line(tracker_fd=l111l11l1ll11lllIl1l1, pipe_handle=lll111l111111l11Il1l1)


        l11ll11l11llll1lIl1l1 = str(Path(l1l1ll1111l1lll1Il1l1['sys_argv'][0]).absolute())
        l1llll1ll111l1l1Il1l1 = [l1llll1ll111l1l1Il1l1[0], '-B', '-m', 'reloadium_launcher', 'spawn_process', str(l111l11l1ll11lllIl1l1), 
str(lll111l111111l11Il1l1), l11ll11l11llll1lIl1l1]
        llll111l11l1l111Il1l1._fds.extend([lll111l111111l11Il1l1, l111ll1ll1l1ll1lIl1l1])
        llll111l11l1l111Il1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
l1llll1ll111l1l1Il1l1, llll111l11l1l111Il1l1._fds)
        llll111l11l1l111Il1l1.sentinel = lll1lll1ll111lllIl1l1
        with open(ll1111ll1l111l11Il1l1, 'wb', closefd=False) as lll1111lll11l1l1Il1l1:
            lll1111lll11l1l1Il1l1.write(llll1lll11l11ll1Il1l1.getbuffer())
    finally:
        l11lllllll11111lIl1l1 = []
        for ll1ll11lllllllllIl1l1 in (lll1lll1ll111lllIl1l1, ll1111ll1l111l11Il1l1, ):
            if (ll1ll11lllllllllIl1l1 is not None):
                l11lllllll11111lIl1l1.append(ll1ll11lllllllllIl1l1)
        llll111l11l1l111Il1l1.finalizer = util.Finalize(llll111l11l1l111Il1l1, l1ll11l1ll1lll1lIl1l1, l11lllllll11111lIl1l1)

        for ll1ll11lllllllllIl1l1 in (lll111l111111l11Il1l1, l111ll1ll1l1ll1lIl1l1, ):
            if (ll1ll11lllllllllIl1l1 is not None):
                os.close(ll1ll11lllllllllIl1l1)


def __init__(llll111l11l1l111Il1l1, l11llllll1llllllIl1l1):
    from reloadium.lib.environ import env
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    from multiprocessing.popen_spawn_win32 import TERMINATE, WINEXE, WINSERVICE, WINENV, _path_eq
    from pathlib import Path
    import os
    import msvcrt
    import sys
    import _winapi

    env.sub_process += 1
    env.save_to_os_environ()

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
        from multiprocessing.popen_spawn_win32 import _close_handles
    else:
        from multiprocessing import semaphore_tracker as tracker 
        _close_handles = _winapi.CloseHandle

    l1l1ll1111l1lll1Il1l1 = spawn.get_preparation_data(l11llllll1llllllIl1l1._name)







    (lll11l1lll1lll11Il1l1, l11l11llllllllllIl1l1, ) = _winapi.CreatePipe(None, 0)
    l1l1l11lllll11llIl1l1 = msvcrt.open_osfhandle(l11l11llllllllllIl1l1, 0)
    llll11111l1lll1lIl1l1 = spawn.get_executable()
    l11ll11l11llll1lIl1l1 = str(Path(l1l1ll1111l1lll1Il1l1['sys_argv'][0]).absolute())
    l1llll1ll111l1l1Il1l1 = ' '.join([llll11111l1lll1lIl1l1, '-B', '-m', 'reloadium_launcher', 'spawn_process', str(os.getpid()), 
str(lll11l1lll1lll11Il1l1), l11ll11l11llll1lIl1l1])



    if ((WINENV and _path_eq(llll11111l1lll1lIl1l1, sys.executable))):
        llll11111l1lll1lIl1l1 = sys._base_executable
        env = os.environ.copy()
        env['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        env = None

    with open(l1l1l11lllll11llIl1l1, 'wb', closefd=True) as ll1111lllll11ll1Il1l1:

        try:
            (l1l111ll1111l1l1Il1l1, l11111ll1111llllIl1l1, ll111l1lllllllllIl1l1, lll1l1lll1l1l111Il1l1, ) = _winapi.CreateProcess(llll11111l1lll1lIl1l1, l1llll1ll111l1l1Il1l1, None, None, False, 0, env, None, None)


            _winapi.CloseHandle(l11111ll1111llllIl1l1)
        except :
            _winapi.CloseHandle(lll11l1lll1lll11Il1l1)
            raise 


        llll111l11l1l111Il1l1.pid = ll111l1lllllllllIl1l1
        llll111l11l1l111Il1l1.returncode = None
        llll111l11l1l111Il1l1._handle = l1l111ll1111l1l1Il1l1
        llll111l11l1l111Il1l1.sentinel = int(l1l111ll1111l1l1Il1l1)
        if (sys.version_info > (3, 8, )):
            llll111l11l1l111Il1l1.finalizer = util.Finalize(llll111l11l1l111Il1l1, _close_handles, (llll111l11l1l111Il1l1.sentinel, int(lll11l1lll1lll11Il1l1), 
))
        else:
            llll111l11l1l111Il1l1.finalizer = util.Finalize(llll111l11l1l111Il1l1, _close_handles, (llll111l11l1l111Il1l1.sentinel, ))



        set_spawning_popen(llll111l11l1l111Il1l1)
        try:
            reduction.dump(l1l1ll1111l1lll1Il1l1, ll1111lllll11ll1Il1l1)
            reduction.dump(l11llllll1llllllIl1l1, ll1111lllll11ll1Il1l1)
        finally:
            set_spawning_popen(None)
