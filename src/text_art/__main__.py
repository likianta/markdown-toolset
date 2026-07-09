import pyfiglet
from argsense import cli


@cli
def fav_all(text: str) -> None:
    fonts = (
        'ansi_shadow',
        'double_blocky',
        'pagga',
        'smmono12',
        'smbraille',
        'big_money-ne',
        'basic',
        'wideterm',
        'smblock',
        'ansi_regular',
        'clr6x6',
        'electronic',
        'dos_rebel',
        'char1___',
        'poison',
        'soft',
        'fender',
        'elite',
    )
    for i, f in enumerate(fonts, 1):
        _divider(i, f)
        print()
        print(pyfiglet.figlet_format(text, font=f))
        print()


@cli
def fav_lite(text: str) -> None:
    fonts = (
        'double_blocky',
        'pagga',
        'smbraille',
        'wideterm',
        'smblock',
        'clr6x6',
        'elite',
    )
    for i, f in enumerate(fonts, 1):
        _divider(i, f)
        print()
        print(pyfiglet.figlet_format(text, font=f))
        print()


@cli
def one(text: str, font: str) -> None:
    print(pyfiglet.figlet_format(text, font=font))


def _divider(index: int, font_name: str, console_width: int = 40) -> None:
    main_text = '{}. {}'.format(index, font_name)
    div_len_left = (console_width - len(main_text) - 2) // 2
    div_len_right = div_len_left + (console_width - len(main_text) - 2) % 2
    final_text = '{} {} {}'.format(
        '-' * div_len_left, main_text, '-' * div_len_right
    )
    print(final_text)


if __name__ == '__main__':
    cli.run()
