import io
import os.path
import pyperclip
import re
import typing as tp

from PIL import ImageGrab
from PIL.Image import Image
from lk_utils import fs
from lk_utils import slice_text
from lk_utils import timestamp


def add_content_to_clipboard(text: str) -> None:
    # https://stackoverflow.com/a/9409898/9695911
    # subprocess.check_call(f'echo | set /p nul={link}| clip', shell=True)
    pyperclip.copy(text)


def format_link(doc_dir: str, link_pattern: str) -> tp.Tuple[str, str]:
    def _substitute(m):
        match m.group(1):
            # case 'bare_name':
            #     return fs.barename(md_file)
            case 'extension':
                return 'png'
            # case 'file_name':
            #     return fs.basename(md_file)
            case 'hns':
                return timestamp('hns')
            # case 'img_dirname':
            #     return fs.dirname(img_root or md_file)
            case 'ymd-hns':
                return timestamp('ymd-hns')[2:]
            case 'ymd_hns':
                return timestamp('ymd_hns')[2:]
            case 'ymdhns':
                return timestamp('ymdhns')[2:]
            case _:
                raise NotImplementedError(m)
    
    link = re.sub(r'<([-\w]+)>', _substitute, link_pattern)
    relpath = slice_text(link).find('(').end().cut().rfind(')').slice()
    img_path = fs.normpath('{}/{}'.format(doc_dir, relpath))
    return img_path, link


def grab_and_save_image(file: str) -> None:
    """
    grab image from clipboard, save to `file`.
    """
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image):
        assert not fs.exist(file)
        img.save(file)
    else:
        file_i = img[0]
        file_o = file
        assert fs.exist(file_i) and not fs.exist(file_o)
        fs.copy_file(file_i, file_o)


def grab_image() -> bytes:
    img = ImageGrab.grabclipboard()
    assert img
    if isinstance(img, Image):
        with io.BytesIO() as f:
            img.save(f, 'png')
            f.seek(0)
            return f.read()
    else:
        # e.g. when we copied an wechat image, the clipboard gives:
        #   [str absolute_file_path]
        assert os.path.isabs(img[0])
        return fs.load(img[0], 'binary')
