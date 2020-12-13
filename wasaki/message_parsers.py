import re


def arg_parser(mes: str) -> (dict, list, set):
    mes = re.findall(r'[^\s"]+|"[^"]*"', mes)
    i = 0
    length = len(mes)
    flags = set()
    params = {}
    inputs = []
    try:
        while i < length:
            if mes[i].startswith("--"):
                flags.add(mes[i][2:])
            elif mes[i].startswith("-"):
                params[mes[i][1:]] = mes[i + 1].replace('"', "")
                i += 1
            elif mes[i].startswith('"') and mes[i].endswith('"'):
                inputs.append(mes[i][1:-1])
            else:
                inputs.append(mes[i])
            i += 1
    except IndexError:
        raise Exception("Invalid Syntax")
    return (params, inputs, flags)
