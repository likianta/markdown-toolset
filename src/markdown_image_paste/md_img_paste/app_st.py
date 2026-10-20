if __name__ == '__main__':
    __package__ = 'src.markdown_image_paste.md_img_paste'

import typing as tp

import streamlit as st
import streamlit_canary as sc
from lk_utils import fs
from neoprint import print

from .common import add_content_to_clipboard
from .common import format_link
from .common import grab_and_save_image
from .common import grab_image


@sc.init_state
class State:
    image_root = ''
    link_format = ''


def main() -> None:
    st.set_page_config('Markdown Image Paste')

    with sc.void_container():
        img_root = _image_root()
        if not img_root:
            return

        doc_dir = _document_dirpath(img_root)
        if not doc_dir:
            return

        link_fmt = _link_format(img_root, doc_dir)

        with sc.columns(2) as cols:
            with cols[0]:
                do_preview = st.button('Preview', use_container_width=True)
            with cols[1]:
                do_dump = st.button(
                    'Dump image',
                    disabled=True if not img_root or not link_fmt else False,
                    use_container_width=True,
                    type='primary',
                )

    info_area = st.empty()
    img_area = st.empty()

    if do_preview or do_dump:
        try:
            with img_area:
                st.image(grab_image())
        except AssertionError:
            with info_area:
                st.error('No image found in the clipboard.')
            return
    if do_dump:
        img_file, link = format_link(doc_dir, link_fmt)
        print(':vn', img_file, link)
        grab_and_save_image(img_file)
        print(':iv2', link)
        add_content_to_clipboard(link)
        with info_area:
            st.success('Saved link: `{}`'.format(link))


def _document_dirpath(image_root: str) -> tp.Optional[str]:
    path = st.text_input('Document path', '$image_parent')
    if path:
        if path == '$image_parent':
            return fs.parent(image_root)
        elif fs.isdir(path):
            return fs.abspath(path)
        elif fs.isfile(path):
            return fs.parent(path)
    st.error('Invalid file path.')
    return None


def _image_root() -> tp.Optional[str]:
    root = st.text_input('Image root')
    if root:
        if fs.isdir(root):
            return fs.abspath(root)
        else:
            st.error('Invalid directory path.')
    else:
        st.markdown(':gray[Input root path to continue.]')
    return None


def _link_format(image_root: str, document_dir: str) -> str:
    relpath = fs.relpath(image_root, document_dir)
    options = (
        '![]({}/<ymd-hns>.<extension>)'.format(relpath),
        '![]({}/<hns>.<extension>)'.format(relpath),
        '![]({}/<source_name_hash>/<ymd-hns>.<extension>)'.format(relpath),
        '![]({}/<source_name_hash>/<hns>.<extension>)'.format(relpath),
    )
    if not relpath.startswith('..'):
        options += tuple(x.replace('(', '(./', 1) for x in options)
    return st.selectbox(
        'Link format',
        options,
        index=0,
        accept_new_options=True,
        help=(
            """
            Supported variants:

            | Variant              | Example       |
            | -------------------- | ------------- |
            | `<source_name_hash>` | 2f448371      |
            | `<ymd_hns>`          | 260721_174820 |
            | `<hns>`              | 174820        |
            | `<extension>`        | png           |
            """
        ),
    )


if __name__ == '__main__':
    # strun 2164 src/markdown_image_paste/md_img_paste/app_st.py
    main()
