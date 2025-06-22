import pyperclip
import qmlease as q
import re
from PIL import ImageGrab
from argsense import cli
from lk_utils import fs
from lk_utils.time_utils import timestamp


@cli
def main(debug: bool = False) -> None:
    q.app.set_app_icon(fs.xpath('../python-holo.ico'))
    q.app.register(Backend())
    q.app.run(fs.xpath('qml/Main.qml'), debug=debug)


class Backend(q.QObject):
    img_root: str
    
    @q.slot(object)
    def init_ui(self, item: q.QObject) -> None:
        @q.bind_signal(item.imageRootChanged)
        def _(path):
            # print(path, ':v')
            if fs.isdir(path) and fs.exist(path):
                item['isValidPath'] = True
                self.img_root = fs.normpath(path)
                print(self.img_root)
            else:
                item['isValidPath'] = False
                self.img_root = ''
        
        @q.bind_signal(item.clicked)
        def _():
            assert self.img_root
            
            # grab image from clipboard
            img = ImageGrab.grabclipboard()
            file = '{}/{}.png'.format(self.img_root, timestamp('hns'))
            img.save(file)
            
            link = self._format_link(file, item['imageLinkFormat'])
            print(':iv2', link)
            # # https://stackoverflow.com/a/9409898/9695911
            # subprocess.check_call(f'echo | set /p nul={link}| clip', shell=True)
            pyperclip.copy(link)
            item['imageLink'] = link
    
    def _format_link(self, file, fmt):
        def _substitute(m):
            match m.group(1):
                case 'img_root_name':
                    return fs.dirname(self.img_root)
                case 'img_file_name':
                    return fs.barename(file)
                case 'img_file_ext':
                    return 'png'
                case _:
                    raise NotImplementedError(m)
        
        return re.sub(r'<(\w+)>', _substitute, fmt)


if __name__ == '__main__':
    # pox src/markdown_image_paste/md_img_paste/main.py
    # pox src/markdown_image_paste/md_img_paste/main.py --debug
    cli.run(main)
