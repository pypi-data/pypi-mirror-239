import json
import re


def assign_value_to_variable(var, var_key, var_value=None, is_assign=False):
    if type(var) is not dict:
        var = dict()

    if is_assign:
        var[var_key] = var_value
    else:
        if var_key not in var:
            var[var_key] = dict()

    return var[var_key]


pattern = re.compile(r'\[([а-яА-Яa-zA-Z0-9_]+)]')


def parse_var_name(var_name):
    return var_name.split('[', 1)[0], pattern.findall(var_name)


def create_var_name(path):
    name = path.pop(0)
    for p in path:
        name = f'{name}[{p}]'
    return name


def parse_var_to_list(var, path=None, var_list=None):
    if path is None: path = []
    if var_list is None: var_list = []
    if type(var) is dict:
        for k in var:
            copied_path = path.copy()
            copied_path.append(k)
            var_list = parse_var_to_list(var[k], copied_path, var_list)
    else:
        var_list.append({
            "name": create_var_name(path),
            "value": var
        })
    return var_list


class Context:
    variables: dict

    def __init__(self, variables=None, ctx: "Context" = None):
        self.parent = ctx
        if type(variables) is dict:
            self.variables = variables
        else:
            self.variables = dict()

    def set(self, var_name, var_value):
        main, add = parse_var_name(var_name)
        len_add = len(add)

        var = assign_value_to_variable(self.variables, main)

        for c, r in enumerate(add, 1):
            if len_add == c:
                var = assign_value_to_variable(var, r, var_value, True)
            else:
                var = assign_value_to_variable(var, r)

    def get(self, var_name):
        main, add = parse_var_name(var_name)
        var = None
        if main in self.variables:
            var = self.variables[main]
            for n in add:
                var = var.get(n)
        return var


if __name__ == "__main__":
    with open('./context.json', encoding='utf-8') as f:
        context = Context(json.load(f))
        vars_list = parse_var_to_list(context.variables)
        with open('./variable.json', 'w', encoding='utf-8') as outfile:
            json.dump(vars_list, outfile, ensure_ascii=False, indent=4)
            context_reload = Context()
            for v in vars_list:
                context_reload.set(v.get("name"), v.get("value"))
            with open('./context_reload.json', 'w', encoding='utf-8') as file:
                json.dump(context_reload.variables, file, ensure_ascii=False, indent=4)
