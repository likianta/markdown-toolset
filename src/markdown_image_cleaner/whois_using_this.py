import re

from lk_utils import fs
from lk_utils import tp


def whois_using_image_dir(img_dir: str):
    parent_dir = fs.parent(img_dir)
    link_fmt = re.compile(
        r'!\[]\((?:\./)?{}/[^)]+\)'.format(fs.basename(img_dir))
    )
    for f in fs.find_files(parent_dir, '.md'):
        content = fs.load(f.path)
        if link_fmt.search(content):
            print(f.relpath, ':iv6')


def whois_using_image_file(img_file: str, search_dir: tp.Optional[str] = None):
    if not search_dir:
        search_dir = fs.parent(fs.parent(img_file))
        print(search_dir, ':n')

    img_name = fs.barename(img_file)
    for f in fs.find_files(search_dir, '.md'):
        doc = fs.load(f.path)
        if img_name in doc:
            print(f.relpath, ':iv6')
