def match(pattern, text):
    """
    Return True if pattern appears at the start of text
    
    Please fill in the last line in this program.
    Namely: match(             ,           )

    We'll explain how we came to the code for the condition:
    elif len(pattern) > 1 and pattern[1] in '*?' in the next video lecture
    """

    if pattern == '':
        return True
    elif pattern == '$':
        return (text == '')
    elif len(pattern) > 1 and pattern[1] in '*?':
        p, op, pat = pattern[0], pattern[1], pattern[2:]
        if op == '*':
            return match_star(p, pat, text)
        elif op == '?':
            if match1(p, text) and match(pat, text[1:]):
                return True
            else:
                return match(pat, text)
    else:
        return (match1(pattern[0], text) and
                match( pattern[1] , text[1:] )) # fill in this line