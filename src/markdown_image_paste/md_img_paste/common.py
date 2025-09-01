import io
import os.path
import pyperclip
import re
from PIL import ImageGrab
from PIL.Image import Image
from lk_utils import fs
from lk_utils import timestamp


def add_content_to_clipboard(text: str) -> None:
    # https://stackoverflow.com/a/9409898/9695911
    # subprocess.check_call(f'echo | set /p nul={link}| clip', shell=True)
    pyperclip.copy(text)


def grab_and_save_image(root: str) -> str:
    """
    grab image from clipboard, save to `<root>/<auto_name>.<ext>`.
    """
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image):
        file_o = '{}/{}.png'.format(root, timestamp('hns'))
        assert not fs.exist(file_o)
        img.save(file_o)
    else:
        file_i = img[0]
        file_o = '{}/{}.{}'.format(
            root, timestamp('hns'), file_i.rsplit('.', 1)[1]
        )
        assert fs.exist(file_i) and not fs.exist(file_o)
        fs.copy_file(file_i, file_o)
    return file_o


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


def format_link(file: str, fmt: str, img_root: str = None) -> str:
    def _substitute(m):
        match m.group(1):
            case 'bare_name':
                return fs.barename(file)
            case 'file_ext':
                return 'png'
            case 'file_name':
                return fs.basename(file)
            case 'root_name':
                return fs.dirname(img_root or file)
            case _:
                raise NotImplementedError(m)
    
    return re.sub(r'<(\w+)>', _substitute, fmt)
