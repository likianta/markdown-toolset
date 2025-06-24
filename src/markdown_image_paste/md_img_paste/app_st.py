if __name__ == '__main__':
    __package__ = 'src.markdown_image_paste.md_img_paste'

import streamlit as st
# import typing as t
from lk_utils import dedent
from lk_utils import fs
from .common import add_content_to_clipboard
from .common import format_link
from .common import grab_and_save_image
from .common import grab_image


def main() -> None:
    img_root = _get_image_root()
    target = _get_target_dir(img_root) if img_root else None
    link_fmt = _get_link_format(img_root, target)
    
    cols = iter(st.columns(2))
    with next(cols):
        do_preview = st.button('Preview', use_container_width=True)
    with next(cols):
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
        link = format_link(file, link_fmt, img_root)
        print(':iv2', link)
        add_content_to_clipboard(link)
        with info_area:
            st.success('Saved link: `{}`'.format(link))


def _get_image_root() -> str | None:
    x = st.text_input('Image root')
    if x and fs.isdir(x):
        return fs.abspath(x)
    return None


def _get_link_format(img_root: str, target_ref: str | None) -> str:
    if target_ref:
        if img_root.startswith(target_ref + '/'):
            prefix = './'
        else:
            prefix = ''
        default_fmt = '![]({}{}/<file_name>)'.format(
            prefix, fs.relpath(img_root, target_ref),
        )
    else:
        default_fmt = '![](./{}/<file_name>)'.format(fs.basename(img_root))
    assert default_fmt.startswith(('![](./', '![](../'))
    
    x = st.text_input(
        'Link format',
        placeholder=default_fmt,
        help=dedent(
            '''
            Supported variants:

            | Variant       | Example    |
            | ------------- | ---------- |
            | `<root_name>` | _assets    |
            | `<file_name>` | 110923.png |
            | `<bare_name>` | 110923     |
            | `<file_ext>`  | png        |
            '''
        )
    )
    return x or default_fmt


def _get_target_dir(img_root: str) -> str:
    usable_dirs = ['..']
    for d in fs.findall_dirs(fs.parent(img_root)):
        if not d.name.startswith(('.', '_')):
            usable_dirs.append(d)
    x = st.selectbox(
        'Select target directory (optional)',
        usable_dirs,
        format_func=lambda x:
        x if isinstance(x, str) else '../{}'.format(x.relpath),
        # disabled=len(usable_dirs) <= 1,
    )
    if x == '..':
        return fs.parent(img_root)
    else:
        return x.abspath


if __name__ == '__main__':
    # strun 2160 src/markdown_image_paste/md_img_paste/app_st.py
    # pox -m pyapp_window --port 3001 --size 750x250 --title
    #   "Markdown Image Paste"
    main()
