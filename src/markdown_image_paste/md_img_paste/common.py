import io
import pyperclip
import re
from PIL import ImageGrab
from lk_utils import fs
from lk_utils import timestamp


def add_content_to_clipboard(text: str) -> None:
    # https://stackoverflow.com/a/9409898/9695911
    # subprocess.check_call(f'echo | set /p nul={link}| clip', shell=True)
    pyperclip.copy(text)


def grab_and_save_image(root: str) -> str:
    """
    grab image from clipboard, save to `<root>/<auto_name>.png`.
    """
    img = ImageGrab.grabclipboard()
    file = '{}/{}.png'.format(root, timestamp('hns'))
    assert not fs.exist(file)
    img.save(file)
    return file


def grab_image() -> bytes:
    img = ImageGrab.grabclipboard()
    assert img
    with io.BytesIO() as f:
        img.save(f, 'png')
        f.seek(0)
        return f.read()


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
