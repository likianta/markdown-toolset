if __name__ == '__main__':
    __package__ = 'src.markdown_image_paste.md_img_paste'

import streamlit as st
import streamlit_canary as sc
from lk_utils import fs

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
        img_root = sc.path_input('Image root')
        if not img_root:
            st.markdown(':gray[Input root path to continue.]')
            return
        elif not fs.isdir(img_root):
            st.error('Invalid directory path.')
            return

        with sc.columns((3, 7)) as cols:
            with cols[0]:
                target_dirpath = _get_target_dir(img_root)
            with cols[1]:
                link_fmt = _get_link_format(img_root, target_dirpath)

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
        file = grab_and_save_image(img_root)
        link = format_link(file, img_root, link_fmt)
        print(':iv2', link)
        add_content_to_clipboard(link)
        with info_area:
            st.success('Saved link: `{}`'.format(link))


def _get_image_root() -> str | None:
    x = st.text_input('Image root')
    if x and fs.isdir(x):
        return fs.abspath(x)
    return None


def _get_link_format(img_root: str, target_dirpath: str) -> str:
    relpath = fs.relpath(img_root, target_dirpath)
    options = (
        '![]({}/<ymd_hns>.<extension>)'.format(relpath),
        '![]({}/<hns>.<extension>)'.format(relpath),
        '![]({}/<source_name_hash>/<ymd_hns>.<extension>)'.format(relpath),
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


def _get_target_dir(img_root: str) -> str:
    usable_dirs = ['..']
    for d in fs.findall_dirs(fs.parent(img_root)):
        if not d.name.startswith(('.', '_')):
            usable_dirs.append('../{}'.format(d.relpath))
    x = st.selectbox('Select target directory (optional)', usable_dirs)
    return x.replace('..', fs.parent(img_root), 1)


if __name__ == '__main__':
    # strun 2164 src/markdown_image_paste/md_img_paste/app_st.py
    main()
