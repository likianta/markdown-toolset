from argsense import cli
from lk_utils import normpath


def md2md(file_i, file_o=''):
    """
    params:
        file_i: an absolute or relative path.
        file_o: 
            optional. if not given, will use the same name as source but ends -
            with '.b64.html'.
            you can also give directory instead of file, it generates -
            '<the_given_dir>/<source_name>.b64.html'.
    """
    from . import md_2_md

    file_i = normpath(file_i)
    file_o = normpath(file_o) if file_o else file_i[:-3] + '.b64.md'
    return md_2_md(file_i, file_o)


def md2html(file_i, file_o=''):
    """
    params:
        file_i: see `@md2md:file_i`
        file_o: see `@md2md:file_o`
    """
    from . import md_2_html

    file_i = normpath(file_i)
    file_o = normpath(file_o) if file_o else file_i[:-3] + '.b64.html'
    return md_2_html(file_i, file_o)


def html2html(file_i, file_o: str = '') -> str:
    """
    params:
        file_i: see `@md2md:file_i`
        file_o: see `@md2md:file_o`
    """
    from . import html_2_html

    file_i = normpath(file_i)
    file_o = normpath(file_o) if file_o else file_i[:-5] + '.b64.html'
    return html_2_html(file_i, file_o)


if __name__ == '__main__':
    # python -m src.markdown_image_base64.md_img_b64 -h
    # python -m src.markdown_image_base64.md_img_b64 md2html ...
    cli.run()
