"""
Notes:
    If new version of pyportable-crypto installed, remember to delete
    "~/lib/pyportable_crypto" to make sure `pyportable_installer.path_model
    .PyPortablePathModel.build_dirs` generate new one.
"""
import os

import pyportable_crypto
from lk_logger import lk
from lk_utils import run_cmd_args


def mainloop(key, root_dir='../pyportable_installer/compilers/lib'):
    _check_crypto_version()
    
    while python_dir := input('system python dir (empty to escape loop): '):
        # you can use `[<major>.<minor>]` (e.g. '[3.8]') to tell program to auto
        # find the specific python version. if auto finding failed, program will
        # continue the loop.
        if python_dir.startswith('['):
            try:
                python_dir = _auto_find_python_path(python_dir[1:-1])
            except FileNotFoundError:
                lk.logt('[E0039]', 'cannot find the specific python version, '
                                   'please check your input and try again.')
                continue
        
        python_exe = f'{python_dir}\\python.exe'
        pyversion = _get_pyversion(python_exe)
        assert os.path.exists(python_exe)
        
        lk.logdx(pyversion)
        dir_o = root_dir + '/pyportable_runtime_' + pyversion
        pyportable_crypto.cipher_gen.generate_custom_cipher_package(
            key, dir_o, python_exe
        )


def _check_crypto_version():
    """ require pyportable_crypto version >= 1.0 """
    ver_segs = pyportable_crypto.__version__.split('.')
    assert float('.'.join(ver_segs[:2])) >= 1.0
    del ver_segs
    return True


def _get_pyversion(python_path) -> str:
    pyversion = run_cmd_args(python_path, '--version')
    # -> e.g. 'Python 3.8.0'
    pyversion = tuple(map(int, pyversion.split(' ')[1].split('.')[:2]))
    # -> e.g. (3, 8)
    pyversion = 'py{}{}'.format(*pyversion)
    # -> e.g. 'py38'
    return pyversion


def _auto_find_python_path(pyversion):
    """
    Args:
        pyversion: str['3.8', '3.9', '3.10']
    """
    from platform import system
    if system().lower() == 'windows':
        path = run_cmd_args(
            'py', f'-{pyversion}', '-c', 'import sys; print(sys.executable)'
        )
        if ' not found!' in path:
            ''' e.g.
                Python 3.11 not found!
                Installed Pythons found by py Launcher for Windows
                 -3.10-64 *
                 -3.9-64
                 -3.8-64
                 -2.7-64
            '''
            raise FileNotFoundError(path)
        return path
    else:
        path = f'/usr/bin/python{pyversion}'
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        return path


if __name__ == '__main__':
    from secrets import token_urlsafe
    
    mainloop(key=token_urlsafe())
    # mainloop(key_='we1c0me_to_depsland', auto_move_to_accessory=False)
