from grako import parse
from grako.exceptions import FailedParse

GRAMMAR = '''
    start = first_term second_term;

    first_term = "%d" | "%f";
    second_term = "+" first_term | "-" first_term;
'''


def generate_code(grammar, text):
    try:
        ast = parse ( text, grammar )
        return ast.as_python ()
    except FailedParse:
        return None


code = generate_code ( GRAMMAR, "3.14 - 1.5" )
print ( code )
