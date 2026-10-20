import re
import streamlit_canary as sc
from lk_utils import fs, uuid


def main_ui():
    sc.PageTitle('Markdown Image Lofter')
    inp = sc.PathInputBrowse(
        'Choose a ".md" file', fs.parent('.'), filter='.md'
    )

    doc_out = sc.Property('')

    with sc.Button('Parse', width='stretch', type='primary') as btn:
        @btn.on_click
        def _():
            file = inp.value.get()
            assert file and file.endswith('.md') and fs.exist(file)
            doc = fs.load(file, 'plain')
            if _detect_image_links(doc):
                temp_dir = fs.there('../data/{}'.format(uuid()[::4]))
                fs.make_dir(temp_dir)
                doc_out.set(
                    _translate_image_links(
                        doc, fs.parent(file), temp_dir
                    )
                )
            else:
                sc.toast('No image link found in this document.')

    with sc.Container(
        border=True, visible=sc.bind(doc_out, bool, default=False), height=800
    ):
        sc.Text(sc.bind(doc_out))


def _detect_image_links(doc):
    return bool(re.search(r'!\[.*?]\((.+)\)', doc))

def _parse_document():
    ...

def _get_image_links(doc: str):
    ...

def _translate_image_links(doc: str, doc_dir_i, img_dir_o):
    
    def _abspath(relpath):
        out = fs.normpath('{}/{}'.format(doc_dir_i, relpath))
        assert fs.exist(out), (doc_dir_i, relpath)
        return out
    
    def _copy_file(file_i):
        file_o = '{}/{}.{}'.format(
            img_dir_o, 
            uuid('{}:{}'.format(file_i, fs.filetime(file_i)))[::4],
            fs.split(file_i, 3)[-1]
        )
        fs.make_link(file_i, file_o)
        return 'http://47.102.108.149:2167/{}/{}'.format(
            fs.dirname(img_dir_o), fs.filename(file_o)
        )

    def _format_link(path):
        return '![]({})'.format(path)

    def _is_local_file(relpath):
        return not relpath.startswith('http')

    doc_out = re.sub(
        r'!\[.*?]\((.+)\)',
        lambda m: (
            _format_link(_copy_file(_abspath(m.group(1)))) 
            if _is_local_file(m.group(1)) 
            else m.group(0)
        ),
        doc
    )
    return doc_out


if __name__ == '__main__':
    sc.run(main_ui, port=2166)
