# --------------
# User Instructions
#
# Write a function, compile_word(word), that compiles a word
# of UPPERCASE letters as numeric digits. For example:
# compile_word('YOU') => '(1*U + 10*O +100*Y)' 
# Non-uppercase words should remain unchaged.

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    words = word.split()
    result = ''
    
    for w in words:
        if (not w.isupper()) or (not w.isalpha()):
            result += w
            continue

        w = w[::-1]
        result += '(' + '+'.join( ['%(n)d*%(l)s'%{"n" : 10**i, "l" : w[i]} for i,l in enumerate(w)] ) + ')'
    
    return result

print compile_word('HOLA + lower')