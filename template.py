from io import StringIO
from contextlib import redirect_stdout
from textwrap import dedent


S_TEXT = 1
S_EVAL = 2


def _run_code(code, vars):
    buf = StringIO()

    with redirect_stdout(buf):
        exec(dedent(code), vars)

    return buf.getvalue()


def tpl(tpl, vars={}):
    """
    Extremely simple templating language.

    **Warning**: Templates are executed as code. Do not use with untrusted
    input.

    The major downside to this templating method is that you cannot mix normal
    output with logic-blocks. Once in a {% %} block, you must use normal python
    output functions (print, sys.stdout) to write output.

    Example:

            template = '''\
            Hello, {{ name }}!

            {%
                for i in items:
                    print(f"* Item #{i}")
            %}

            Bye.
            '''

            rendered = tpl(
                template,
                vars={
                    "name": "world",
                    "items": ["A", "B"]
                }
            )
    """
    out = ""

    state = S_TEXT
    cur_pos = 0
    cur_code = ""
    while cur_pos < len(tpl):
        # Switch states and forward position in template depending on current
        # character
        if tpl[cur_pos] == "{" and tpl[cur_pos + 1] == "{":
            # {{
            state = S_EVAL
            cur_pos += 2
        elif tpl[cur_pos] == "}" and tpl[cur_pos + 1] == "}":
            # }}
            out += _run_code(f"print(str({cur_code}), end='')", vars)
            state = S_TEXT
            cur_code = ""
            cur_pos += 2
        elif tpl[cur_pos] == "{" and tpl[cur_pos + 1] == "%":
            # {%
            state = S_EVAL
            cur_pos += 2
        elif tpl[cur_pos] == "%" and tpl[cur_pos + 1] == "}":
            # %}
            out += _run_code(cur_code, vars)
            state = S_TEXT
            cur_code = ""
            cur_pos += 2
            if tpl[cur_pos] == "\n":
                # Swallow newlines after code block
                cur_pos += 1

        # Consume characters in template depending on state
        try:
            if state == S_EVAL:
                cur_code += tpl[cur_pos]
            elif state == S_TEXT:
                out += tpl[cur_pos]
        except IndexError:
            pass

        cur_pos += 1
    return out


if __name__ == "__main__":
    template = '''\
Hello, {{ name }}!

{%
    for i in items:
        print(f"* Item #{i}")
%}

Bye.
'''

    rendered = tpl(
        template,
        vars={
            "name": "world",
            "items": ["A", "B"]
        }
    )
    import sys
    sys.stdout.write(rendered)

