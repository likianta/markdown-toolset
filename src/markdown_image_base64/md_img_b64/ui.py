if __name__ == '__main__':
    __package__ = 'src.markdown_image_base64.md_img_b64'

import streamlit as st
from lk_utils import fs

from .converter import md_2_html

st.set_page_config('Markdown Export To HTML')

path_i = st.text_input('Input markdown filepath')
path_o = st.text_input('Output HTML filepath (optional)')

if st.button('Export to single-page HTML', disabled=not path_i):
    assert fs.exist(path_i)
    
    if not path_o:
        path_o = fs.replace_ext(path_i, 'b64.html')
    elif fs.isdir(path_o):
        path_o = '{}/{}.b64.html'.format(path_o, fs.barename(path_i))
    
    md_2_html(path_i, path_o)
    st.success('See result at {}'.format(fs.normpath(path_o)))

# strun 2163 projects/markdown_image_base64/md_img_b64/ui.py
