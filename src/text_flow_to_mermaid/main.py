import typing as t
from argsense import cli
from lk_utils import fs
from collections import defaultdict


@cli
def main(file_i: str, file_o: str = None) -> None:
    data_r: str = fs.load(file_i)
    
    _chrx = 64
    curr_graph_key = ''
    # graph_links = {'': []}
    #   {graph_key: {(last_var, curr_var, connect_type), ...}, ...}
    indent_2_var = {}
    links = []  # [(graph1, var1, var2, connect_type), ...]
    text_2_var = {}
    var_2_text = {}  # {alpha_letter: text, ...}
    
    # curr_graph_key = ''
    # curr_links = graph_links['']
    
    def add_new_var(text: str) -> str:
        nonlocal _chrx
        _chrx += 1
        assert _chrx <= 90
        new_var = chr(_chrx)  # 'A' ~ 'Z'
        var_2_text[new_var] = text
        print('{} -> {}'.format(new_var, text), ':pv2i')
        text_2_var[text] = new_var
        indent_2_var[indent] = new_var
        return new_var
    
    # def add_new_graph(key: str) -> None:
    #     nonlocal curr_graph_key, curr_links
    #     assert key not in graph_links
    #     curr_graph_key = key
    #     curr_links = graph_links[key] = []
    
    # def line_2_var(line: str) -> str:
    #     if line[0] == '@':
    #         return text_2_var[line[1:]]
    #     else:
    #         return add_new_var(line)
    
    flag = 'INIT'
    for i, raw_line in enumerate(data_r.splitlines(), 1):
        line, indent = _parse_line(raw_line)
        print(i, line, ':v')
        if not line:
            continue
        match flag:
            case 'INIT':
                if line.endswith(':'):
                    assert curr_graph_key == ''
                    curr_graph_key = line[:-1]
                    flag = 'FLOW_START'
            case 'FLOW_START':
                assert not line.startswith('@')
                assert not line.endswith(':')
                if curr_graph_key:
                    assert indent > 0
                add_new_var(line)
                flag = 'FLOW_GOES_ON'
            case 'FLOW_GOES_ON':
                if indent == 0 and line.endswith(':'):
                    curr_graph_key = line[:-1]
                    flag = 'FLOW_START'
                else:
                    # assert indent > 0
                    assert line.startswith(('-> ', '是: ', '否: '))
                    assert not line.endswith(':')
                    last_var = indent_2_var[indent - 1]
                    if line[3] == '@':
                        # curr_var = text_2_var[line[4:]]
                        curr_var = line[3:]
                    else:
                        curr_var = add_new_var(line[3:])
                    links.append((curr_graph_key, last_var, curr_var, line[0]))
    else:
        assert flag == 'FLOW_GOES_ON'
    
    # -------------------------------------------------------------------------
    
    data_w = ['graph TB;', '']
    
    def wrap_text(text: str) -> str:
        if ' ' in text:
            return '"{}"'.format(text)
        else:
            return text
    
    for var_, text in var_2_text.items():
        data_w.append('{}[{}];'.format(var_, wrap_text(text)))
    data_w.append('')
    
    # classify var to graph
    graphs = defaultdict(list)
    for lnk in links:
        graphs[lnk[0]].append(lnk[1:])
    for key, links in graphs.items():
        if key:
            if data_w[-2] == 'end':
                # move out last row from last graph, join it to the new graph.
                row0 = data_w.pop()  # ''
                row1 = data_w.pop()  # 'end'
                row2 = data_w.pop()  # X -> Y
                data_w.append(row1)
                data_w.append(row0)
                data_w.append(
                    'subgraph {};'.format(wrap_text('**{}**'.format(key)))
                )
                data_w.append(row2)
            else:
                data_w.append(
                    'subgraph {};'.format(wrap_text('**{}**'.format(key)))
                )
        for last_var, curr_var, conn_type in sorted(links):
            if curr_var[0] == '@':
                x = curr_var[1:]
                try:
                    curr_var = text_2_var[x]
                except KeyError as e:
                    if x in graphs:
                        curr_var = graphs[x][0][0]
                    else:
                        raise e
            if conn_type == '-':
                data_w.append('{} --> {};'.format(last_var, curr_var))
            else:
                data_w.append('{} -- {} --> {};'.format(
                    last_var, conn_type, curr_var
                ))
        if key:
            data_w.append('end')
        data_w.append('')
    if data_w[-1] == '':
        data_w.pop()
    
    if file_o:
        fs.dump(data_w, file_o)
    else:
        print('\n' + '```mermaid' + '\n' + '\n'.join(data_w) + '\n' + '```')
    
    
def _parse_line(line: str) -> t.Tuple[str, int]:
    line = line.rstrip()
    indent = (len(line) - len(line.lstrip())) // 4
    return line.strip(), indent


if __name__ == '__main__':
    # pox src/text_flow_to_mermaid/main.py ...
    cli.run(main)
