import string, re

def valid(f):
    "Formula f is valid iff it has no numbers with leading zero and evals true."
    try:
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ZeroDivisionError:
        return False


print valid('1+2==3')
print valid('1+3==3')
print valid('1/0==3')