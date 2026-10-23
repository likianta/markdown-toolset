import re
import streamlit_canary as sc
import typing as tp
from argsense import cli
from functools import partial
from lk_utils import fs, run_cmd_args, uuid


def run(
    enable_file_server: bool = True,
    bore_secret: str = '',
    domain: str = '',
    port: int = 2167,
) -> None:
    """
    Args:
        enable_file_server (-f):
        bore_secret (-s):
        domain (-d): Starting from 'http://' or 'https://'.
            Note: CSDN image hosting requires https links. You can use -
            NAT-DDNS tools (e.g. AweShell, Cpolar) to get a https domain.
        port (-p):
    """
    if not domain:
        domain = (
            f'http://47.102.108.149:{port}'
            if bore_secret
            else f'http://localhost:{port}'
        )
    print(domain, ':n')

    if enable_file_server:
        run_cmd_args(
            (
                'python',
                '-m',
                'http.server',
                '-d',
                'src/markdown_image_lofter/data',
                str(port),
            ),
            verbose=True,
            blocking=False,
        )
        if bore_secret:
            run_cmd_args(
                (
                    'bore',
                    'local',
                    '-s',
                    bore_secret,
                    '-t',
                    '47.102.108.149',
                    '-p',
                    str(port),
                    str(port),
                ),
                verbose=True,
                blocking=False,
            )
    sc.run(partial(main_ui, domain), port=2166)


def main_ui(domain: str = 'http://localhost:2167') -> None:
    sc.PageTitle('Markdown Image Lofter')

    # print(fs.abspath('.'))
    inp = sc.PathInputBrowse(
        'Choose a ".md" file', fs.parent('.'), filter='.md'
    )

    doc_out = sc.Property('')

    with sc.Button('Parse', width='stretch', type='primary') as btn:

        @btn.on_click
        def _():
            doc_file = tp.cast(str, inp.value.get())
            assert doc_file and doc_file.endswith('.md') and fs.exist(doc_file)
            doc = fs.load(doc_file, 'plain')
            if _detect_image_links(doc):
                temp_dir = fs.there('../data/{}'.format(_file_to_id(doc_file)))
                fs.make_dir(temp_dir)
                doc_out.set(
                    _translate_image_links(
                        doc, fs.parent(doc_file), temp_dir, domain
                    )
                )
            else:
                sc.toast('No image link found in this document.')

    sc.TextArea(value=sc.bind(doc_out), height=800)


def _detect_image_links(doc):
    return bool(re.search(r'!\[.*?]\((.+)\)', doc))


def _file_to_id(file: str) -> str:
    return uuid('{}:{}'.format(file, fs.filetime(file)))[::4]


def _parse_document(): ...


def _get_image_links(doc: str): ...


def _translate_image_links(
    doc: str, doc_dir_i, img_dir_o, domain: str = 'http://localhost:2167'
) -> str:

    def _abspath(relpath):
        out = fs.normpath('{}/{}'.format(doc_dir_i, relpath))
        assert fs.exist(out), (doc_dir_i, relpath)
        return out

    def _copy_file(file_i):
        file_o = '{}/{}.{}'.format(
            img_dir_o, _file_to_id(file_i), fs.split(file_i, 3)[-1]
        )
        fs.make_link(file_i, file_o)
        return '{}/{}/{}'.format(
            domain, fs.dirname(img_dir_o), fs.filename(file_o)
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
        doc,
    )
    return doc_out


if __name__ == '__main__':
    # python -m src.markdown_image_lofter.md_img_lofter.app -h
    # python -m src.markdown_image_lofter.md_img_lofter.app -s <bore_secret>
    # python -m src.markdown_image_lofter.md_img_lofter.app \
    #   -d https://ys75786om272.vicp.fun -p 2031
    cli.run(run)
