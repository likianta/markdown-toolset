from lk_utils import fs
from lk_utils import regex as re
from lk_utils import timestamp
from lk_utils import tp


def batch_normalize_filenames(
    folder: str, dry_run: bool = False, respect_original_name: bool = False
):
    """
    params:
        dry_run (-d):
        respect_original_name (-r):
    """
    for f in fs.find_files(folder):
        old_name = f.name
        if respect_original_name:
            ...
        else:
            new_name = '{}.{}'.format(
                timestamp('ymdhns', tp.cast(int, fs.filetime(f.path)))[2:], f.ext
            )
        if new_name == old_name:
            print(f.relpath, 'no change', ':i')
        else:
            print('rename: {} -> {}'.format(old_name, new_name), ':r2i')
            if not dry_run and new_name != old_name:
                fs.move(f.path, '{}/{}'.format(folder, new_name))


def normalize_filename(file: str):
    old_name = fs.basename(file)
    new_name = '{}.{}'.format(
        timestamp('ymdhns', tp.cast(int, fs.filetime(file)))[2:],
        re.slice(old_name).rfind('.').end().cut().slice(),
    )
    print('rename: {} -> {}'.format(old_name, new_name), ':r2')
    fs.move(file, '{}/{}'.format(fs.parent(file), new_name))
