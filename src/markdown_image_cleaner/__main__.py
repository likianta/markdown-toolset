# if 1:
#     print(__package__)

import os.path
import re

from argsense import cli
from lk_utils import fs
from lk_utils import timestamp
from lk_utils import tp

from . import renamer
from . import whois_using_this

cli.add_cmd(whois_using_this.whois_using_image_dir) 
cli.add_cmd(whois_using_this.whois_using_image_file)
cli.add_cmd(renamer.batch_normalize_filenames)
cli.add_cmd(renamer.normalize_filename)


@cli
def remove_all_unused_images(
    docs_root: str, images_root: tp.Optional[str] = None, dry_run: bool = False
):
    assert images_root, 'not implemented'
    all_images = set(fs.findall_file_paths(images_root))
    used_images = set()

    for f in fs.findall_files(docs_root, '.md'):
        content = fs.load(f.path)
        for m in re.finditer(r'!\[.*?]\((.*?)\)', content):
            print(':i', m.group(0))
            if not images_root:
                ...
            abspath = fs.normpath('{}/{}'.format(f.dir, m.group(1)))
            if abspath in all_images:
                used_images.add(abspath)

    for f in sorted(all_images - used_images):
        print(':iv8', fs.relpath(f, images_root))
        if not dry_run:
            _soft_delete(f)


def _soft_delete(file):
    fs.move(file, '{}/{}'.format(fs.xpath('deleted'), fs.basename(file)), True)


@cli
def delete_image_files(md_file: str) -> None:
    md_dir = fs.parent(md_file)
    fs.make_dir(del_dir := fs.xpath('deleted/{}'.format(timestamp('ymd-hns'))))
    content = fs.load(md_file)

    count = 0
    for m in re.finditer(r'!\[.*?]\((.*?)\)', content):
        print(':i', m.group(0))
        possible_path = m.group(1)
        if possible_path.startswith('http'):
            continue
        if os.path.isabs(possible_path):
            path = possible_path
        else:
            if fs.exist(
                x := fs.normpath(
                    '{}/{}'.format(md_dir, possible_path.removeprefix('./'))
                )
            ):
                path = x
            else:
                print(':v6', 'invalid path "{}" in "{}"'.format(x, m.group(0)))
                continue
        fs.move(path, del_dir + '/' + fs.basename(path))
        count += 1

    if count:
        print(':v1t', 'delete {} files, see "{}"'.format(count, del_dir))
    else:
        print(':v7', 'there is no image file to delete')
        fs.remove(del_dir)


if __name__ == '__main__':
    # pox -m markdown_image_cleaner -h
    # pox -m markdown_image_cleaner remove_all_unused_images ...
    cli.run()
