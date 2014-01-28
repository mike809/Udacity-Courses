# -----------
# User Instructions
# 
# Modify the card_ranks() function so that cards with
# rank of ten, jack, queen, king, or ace (T, J, Q, K, A)
# are handled correctly. Do this by mapping 'T' to 10, 
# 'J' to 11, etc...

def card_ranks(cards):
    mapper = { 'A' : '14', 'K' : '13', 'Q' : '12', 'J' : '11', 'T' : '10' }
    ranks = [ mapper[r] if r.isalpha() else r for r,s in cards] 
    return sorted(ranks, reverse = True)
    

print card_ranks(['AC', '3D', '4S', 'KH']) #should output [14, 13, 4, 3]
