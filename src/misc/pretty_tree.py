from argsense import cli
from lk_utils import fs

fs.cd_current_dir()


@cli
def main(
    file_in: str = '_tree_in.txt',
    file_out: str = '_tree_out.txt',
    ruler_width: int = 3,
) -> None:
    """
    params:
        ruler_width (-w): 3 or 4.
    """
    data_r = tuple(fs.load(file_in).splitlines())
    data_w = []

    def fill_width(ruler: str) -> str:
        if ruler_width == 3:
            return ruler
        elif ruler_width == 4:
            if ruler.strip():
                return ruler[:-1] + ruler[-2] + ' '
            else:
                return '    '
        else:
            raise Exception(ruler_width)

    def is_there_same_indent_in_next_lines() -> bool:
        for next_line in data_r[index + 1 :]:
            if _get_indent(next_line) == curr_indent:
                return True
            elif _get_indent(next_line) < curr_indent:
                break
        return False

    col_2_ruler = {}
    #   Dict[indent, ruler]
    #       indent: Int[0, 4, 8, 12, ...]
    #       ruler: Literal["│", "├", "└"]

    for index, curr in enumerate(data_r):
        curr_indent = _get_indent(curr)
        if index == 0:
            assert not curr.startswith('|-')
            data_w.append(curr)
        elif index == 1:
            assert curr.startswith('|-')
            part_a = (
                fill_width('├─ ')
                if is_there_same_indent_in_next_lines()
                else fill_width('└─ ')
            )
            part_b = curr.lstrip().removeprefix('|- ')
            data_w.append(''.join((part_a, part_b)))
            col_2_ruler[curr_indent] = part_a[0]
        else:
            part_a = ''
            for i in range(curr_indent):
                if i % 4 == 0:
                    match col_2_ruler[i]:
                        case '│':
                            raise Exception(index, curr)
                        case '├':
                            part_a += fill_width('│  ')
                        case '└':
                            part_a += fill_width('   ')
            assert part_a
            part_b = (
                fill_width('├─ ')
                if is_there_same_indent_in_next_lines()
                else fill_width('└─ ')
            )
            part_c = curr.lstrip().removeprefix('|- ')
            data_w.append(''.join((part_a, part_b, part_c)))
            col_2_ruler[curr_indent] = part_b[0]

    fs.dump(data_w, file_out)


def _get_indent(line: str, check=True) -> int:
    out = len(line) - len(line.lstrip())
    if check:
        assert out % 4 == 0
    return out


if __name__ == '__main__':
    cli.run(main)
