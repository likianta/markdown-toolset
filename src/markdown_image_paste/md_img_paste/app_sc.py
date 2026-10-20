import typing as tp

import streamlit_canary as sc
from lk_utils import fs
from neoprint import print
from streamlit_canary import components_v3 as v3


class _State(sc.StateV2):
    doc_root: sc.Property[str]
    img_root: sc.Property[str]
    link_fmt: sc.Property[str]


state = _State()


def ui():
    v3.PageTitle('Markdown Image Paste')

    with v3.PathInputBrowse('Image root') as img_root_inp:
        state.img_root.bind(img_root_inp.value)

    with v3.TextInput('Document path', '$image_parent') as doc_path_inp:

        @doc_path_inp.on_submit.emit_now
        def _(value):
            if value == '$image_parent':
                state.doc_root.set(fs.parent(state.img_root.get()))
            elif fs.isdir(value):
                state.doc_root.set(fs.abspath(value))
            elif fs.isfile(value):
                state.doc_root.set(fs.parent(value))
            else:
                sc.toast(sc.red('Invalid file path: {}'.format(value)))

    def _get_options(factors):
        img_root, doc_root = factors
        relpath = fs.relpath(img_root, doc_root)
        options = (
            '![]({}/<ymd-hns>.<extension>)'.format(relpath),
            '![]({}/<hns>.<extension>)'.format(relpath),
            '![]({}/<source_name_hash>/<ymd-hns>.<extension>)'.format(relpath),
            '![]({}/<source_name_hash>/<hns>.<extension>)'.format(relpath),
        )
        if not relpath.startswith('..'):
            options += tuple(x.replace('(', '(./', 1) for x in options)
        return options

    with v3.Selectbox(
        'Link format',
        sc.bind((state.img_root, state.doc_root), _get_options),
        accept_new_option=True,
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
    ) as link_fmt_inp:
        state.link_fmt.bind(link_fmt_inp.value)

    with v3.Grid(cols=2) as grid:
        with next(grid):
            with v3.Button('Preview', width='stretch') as prev_btn:
                ...
        with next(grid):
            with v3.Button(
                'Dump image', width='stretch', type='primary'
            ) as dump_btn:
                ...
    
    with v3.Callout() as info:
        ...

    with v3.Image() as img:
        ...


if __name__ == '__main__':
    sc.run(ui, port=2164)
