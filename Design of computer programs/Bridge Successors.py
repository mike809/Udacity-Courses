# -----------------
# User Instructions
# 
# Write a function, bsuccessors(state), that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# A state is a (here, there, t) tuple, where here and there are 
# frozensets of people (indicated by their times), and potentially
# the 'light,' t is a number indicating the elapsed time.
#
# An action is a tuple (person1, person2, arrow), where arrow is 
# '->' for here to there or '<-' for there to here. When only one 
# person crosses, person2 will be the same as person one, so the
# action (2, 2, '->') means that the person with a travel time of
# 2 crossed from here to there alone.

def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and 
    '<-' for there to here."""
    here, there, t = state
    # your code here  
    b = {}
    flag = False
    if 'light' in here:
        newfrom = list(here)
        newthere = list(there)
    else:
        newfrom = list(there)
        newthere = list(here)
        flag = True

    newfrom.remove('light')
    
    for i in newfrom:
        for j in newfrom:
            newthere.extend([i,j])
            newfrom.remove(i)
            if j in newfrom: newfrom.remove(j)  
            newthere.append('light')

            if not flag:
                b[(frozenset(newfrom),frozenset(newthere), t+max(i,j))] = (i,j,'->')
            else:
                b[(frozenset(newthere),frozenset(newfrom), t+max(i,j))] = (i,j,'<-')

            newthere.remove(i)
    return b

def test():

    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == { 
                (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) =={
                (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}
    
    return 'tests pass'

print test()