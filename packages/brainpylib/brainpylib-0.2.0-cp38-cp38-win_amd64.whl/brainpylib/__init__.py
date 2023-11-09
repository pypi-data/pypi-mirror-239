# -*- coding: utf-8 -*-


__version__ = "0.2.0"

__brainpy_minimal_version__ = '2.4.4.post3'
__minimal_taichi_version__ = (1, 7, 0)

import os
import taichi as ti  # noqa

taichi_path = ti.__path__[0]
taichi_c_api_install_dir = os.path.join(taichi_path, '_lib', 'c_api')
os.environ.update({'TAICHI_C_API_INSTALL_DIR': taichi_c_api_install_dir,
                   'TI_LIB_DIR': os.path.join(taichi_c_api_install_dir, 'runtime')})

if ti.__version__ < __minimal_taichi_version__:
    raise RuntimeError(
        f'We need taichi>={".".join(__minimal_taichi_version__)}. '
        f'Currently you can install taichi>={".".join(__minimal_taichi_version__)} through taichi-nightly:\n\n'
        '> pip install -i https://pypi.taichi.graphics/simple/ taichi-nightly'
    )


def check_brainpy_version():
    import brainpy as bp
    if bp.__version__ < __brainpy_minimal_version__:
        raise RuntimeError(f'brainpylib needs brainpy >= {__brainpy_minimal_version__}, please upgrade it. ')
