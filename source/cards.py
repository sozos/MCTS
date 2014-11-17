HIGH_CARD, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND, STRAIGHT, FLUSH, FULL_HOUSE, FOUR_OF_A_KIND, STRAIGHT_FLUSH = range(9)

import random

class Deck(object):
    def __init__(self, num_decks=1):
        """
        Generate a list of cards for num_decks decks, 52 cards per deck.
    
        codes:
            rank:
                2-10
                11 jack
                12 queen
                13 king
                14 ace
    
            suit:
                (d)iamonds
                (s)pades
                (h)earts
                (c)lubs
            
        Example Deck:
            [(2, 'd'), (4, 's'), ...]
        """
        self.all_cards = []
        for deck in range(num_decks):
            for suit in 'dshc':
                for value in range(2,15):
                    self.all_cards.append((value, suit))
        self.shuffle()
    
    def shuffle(self):
        self.cards = self.all_cards[:]
        random.shuffle(self.cards)
        
    def take(self, n):
        taken = self.cards[:n]
        self.cards = self.cards[n:]
        return taken
        
    def take_one(self):
        taken = self.take(1)
        return taken[0]
                
def is_flush(hand):
    _rank, flush_suit = hand[0]
    for card in hand[1:]:
        _rank, suit = card
        if suit != flush_suit:
            return False
    else:
        return True
        
def is_straight(sorted_hand):
    last_rank, _suit = sorted_hand[0]
    for i, card in enumerate(sorted_hand[1:]):
        rank, _suit = card
        # handle the case of a straight with an ace
        # acting as 1, though its rank is 14:
        # 14, 5, 4, 3, 2
        #     0, 1, 2, 3
        if rank == 5 and i == 0 and last_rank == 14:
            pass
        elif rank != last_rank - 1:
            return False
        last_rank = rank
    else:
        return True
        
def hand_rank(hand):
    """
    Convert a 5 card hand into a tuple representing its relative rank among
    all possible hands. While the magnitude is meaningless, the ordering is
    not, and the tuple tells you if one hand is worth more than another.
    
    This takes advantage of the properties of tuples in Python.  When you
    compare two tuples, the values in the tuple are compared in order until
    one is found that is different from the other, just like comparing strings.
    
    The first number in the tuple is the overall rank of the hand, the other
    numbers are only useful for comparing two hands of the same overall rank,
    for example, two two-pair hands are compared first on the rank of their
    respective pairs, then, if those are equal, on the other cards in the hand.

    This function is not particularly efficient.
    
    Example:
    
        >>> high_card = [(14, 'd'), (10, 'd'), (9, 's'), (5, 'c'), (4, 'c')]
        >>> hand_rank(high_card)
        (0, 14, 10, 9, 5, 4)
        >>> one_pair = [(10, 'c'), (10, 's'), (6, 's'), (4, 'h'), (2, 'h')]
        >>> hand_rank(one_pair)
        (1, 10, 6, 4, 2)
        >>> two_pair = [(13, 'h'), (13, 'd'), (2, 's'), (2, 'd'), (11, 'h')]
        >>> hand_rank(two_pair)
        (2, 13, 2, 11)
        >>> three_of_a_kind = [(8, 's'), (8, 'h'), (8, 'd'), (5, 's'), (3, 'c')]
        >>> hand_rank(three_of_a_kind)
        (3, 8, 5, 3)
        >>> straight = [(8, 's'), (7, 's'), (6, 'h'), (5, 'h'), (4, 's')]
        >>> hand_rank(straight)
        (4, 8)
        >>> flush = [(14, 'h'), (12, 'h'), (10, 'h'), (5, 'h'), (3, 'h')]
        >>> hand_rank(flush)
        (5, 14, 12, 10, 5, 3)
        >>> full_house = [(10, 's'), (10, 'h'), (10, 'd'), (4, 's'), (4, 'd')]
        >>> hand_rank(full_house)
        (6, 10, 4)
        >>> four_of_a_kind = [(10, 'h'), (10, 'd'), (10, 'h'), (10, 's'), (5, 'd')]
        >>> hand_rank(four_of_a_kind)
        (7, 10, 5)
        >>> straight_flush = [(7, 'h'), (6, 'h'), (5, 'h'), (4, 'h'), (3, 'h')]
        >>> hand_rank(straight_flush)
        (8, 7)
    """
    cards = list(reversed(sorted(hand)))
    assert(len(cards) == 5)
    
    # straights/flushes
    straight = is_straight(cards)
    flush = is_flush(cards)
    if straight and flush:
        return (STRAIGHT_FLUSH, cards[0][0])
    elif flush:
        return tuple([FLUSH] + [rank for rank, suit in cards])
    elif straight:
        return (STRAIGHT, cards[0][0])

    # of_a_kind
    histogram = {}
    for card in cards:
        rank, _suit = card
        histogram.setdefault(rank, [])
        histogram[rank].append(card)
    
    of_a_kind = {}
    for rank, cards in reversed(sorted(histogram.items())):
        num = len(cards)
        of_a_kind.setdefault(num, [])
        of_a_kind[num].append(rank)
    
    num = max(of_a_kind)
    ranks = of_a_kind[num]
    if num == 4:
        result = [FOUR_OF_A_KIND]
    elif num == 3:
        if 2 in of_a_kind:
            result = [FULL_HOUSE]
        else:
            result = [THREE_OF_A_KIND]
    elif num == 2:
        if len(ranks) == 1:
            result = [ONE_PAIR]
        if len(ranks) == 2:
            result = [TWO_PAIR]
    elif num == 1:
        result = [HIGH_CARD]
    else:
        raise Exception("Failed to evaluate hand rank")

    result += ranks
    # get the rest of the cards to complete the tuple
    for n in range(num-1, 0, -1):
        if n in of_a_kind:
            result += of_a_kind[n]
    
    return tuple(result)
    
def n_card_rank(cards):
    """
    Find the highest rank for a set of n cards.  Simply ranks all 5 card hands
    in the 7 cards and returns the highest.
    
    >>> n_card_rank([(10, 'h'), (10, 'd'), (10, 'h'), (10, 's'), (5, 'd'), (4, 'd'), (3, 'd')])
    (7, 10, 5)
    >>> n_card_rank([(10, 'h'), (10, 'd'), (10, 'h'), (6, 's'), (5, 'd'), (4, 'd'), (3, 'd')])
    (3, 10, 6, 5)
    >>> n_card_rank([(10, 'h'), (10, 'd'), (10, 'h'), (6, 's'), (5, 'd'), (4, 'd'), (4, 'd')])
    (6, 10, 4)
    >>> n_card_rank([(10, 'h'), (10, 'd'), (10, 'h'), (6, 'd'), (5, 'd'), (4, 'd'), (3, 'd')])
    (5, 10, 6, 5, 4, 3)
    """
    cards = list(reversed(sorted(cards)))
    return max(hand_rank(hand) for hand in choose(5, cards))
    
def choose(n, seq):
    """
    Return all n-element combinations of elements from seq
    
    >>> len(choose(5, [1,2,3,4,5,6,7]))
    21
    """
    if n == 1:
        return [[x] for x in seq]
    if len(seq) <= n:
        return [seq]
    subseq = seq[:]
    elem = subseq.pop()
    return [[elem] + comb for comb in choose(n-1, subseq)] + choose(n, subseq)
    
if __name__ == "__main__":
    import timeit
    t = timeit.Timer(setup='from __main__ import hand_rank', stmt="hand_rank([(10, 'h'), (10, 'd'), (10, 'h'), (10, 's'), (5, 'd')])")
    print "seconds",t.timeit(5*21)
    import doctest
    doctest.testmod()