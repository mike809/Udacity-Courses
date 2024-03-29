# ---------------
# User Instructions
#
# Write a function, n_ary(f), that takes a binary function (a function
# that takes 2 inputs) as input and returns an n_ary function. 

def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        # your code here
        
        if len(args) < 1:
            return x
        
        elif len(args) > 1:
            return f(x, n_ary_f(*args))
        
        else:
            return f(x, *args)

    return n_ary_f
