from shutil import copyfile

from .attachments import copy_attachments
from ....path_model import dst_model
from ....path_model import prj_model
from ....path_model import src_model
from ....typehint import *


def main(conf: TConf, **kwargs):
    """
    
    Args:
        conf:
        **kwargs:

    Keyword Args:
        copy_checkup_tools: bool[True]
        hello
    """
    src_model.assert_ready()
    dst_model.assert_ready()
    
    if src_model.readme:
        _create_readme(src_model.readme, dst_model.readme)
    
    if kwargs.get('copy_checkup_tools', True):
        _copy_checkup_tools(prj_model.checkup, dst_model.build)
    
    # mode = conf['build']['venv']['mode']  # type: TMode
    # options = conf['build']['venv']['options'][mode]
    #
    # if mode in ('source_venv', 'embed_python'):
    #     pass

    pyfiles = []
    pyfiles.extend(_copy_sources(src_model.prj_root, dst_model.prj_root))
    pyfiles.extend(copy_attachments(conf['build']['attachments']))
    return pyfiles


def _copy_checkup_tools(dir_i, dir_o):
    copyfile(
        f'{dir_i}/doctor.py', f1 := f'{dir_o}/doctor.py'
    )
    copyfile(
        f'{dir_i}/pretty_print.py', f2 := f'{dir_o}/pretty_print.py'
    )
    # TODO: add copy: 'update.py'
    return f1, f2


def _create_readme(file_i: TPath, file_o: TPath):
    if file_i.endswith('.md'):
        try:
            # TODO: import a markdown_2_html converter.
            #   https://github.com/likianta/markdown_images_to_base64
            from markdown_images_to_base64 import md_2_html_base64
            file_o = file_o.removesuffix('.md') + '.html'
            #  ~.removesuffix: introduced in Python 3.9.
            md_2_html_base64(file_i, file_o)
        except ImportError:
            copyfile(file_i, file_o)
    else:
        copyfile(file_i, file_o)


def _copy_sources(dir_i, dir_o):
    """
    将 proj_dir 的内容全部拷贝到 src_dir 下, 并返回 src_dir 以及 src_dir 的所有
    子目录.

    Args:
        dir_i: source project directory. i.e. `src_model.prj_root`.
        dir_o: dist project directory. i.e. `dst_model.prj_root`.
    """
    yield from copy_attachments({
        dir_i: {'marks': ('assets', 'compile'), 'path': dir_o}
    })