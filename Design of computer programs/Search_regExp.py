def search(pattern, text):
    """Return true if pattern appears anywhere in text
	   Please fill in the match(          , text) below.
	   For example, match(your_code_here, text)"""
    if pattern.startswith('^'):
        return match( pattern[1:] , text) # fill this line
    else:
        return match( '.*' + pattern , text) # fill this line