"""
Pot class for keeping track of bets and splitting winnings among players.
Should handle any sort of combination of ties and players being all in.
"""

import collections
        
class InsufficientBet(Exception):
    def __init__(self, player, amount):
        self.player = player
        self.amount = amount
        
class AlreadyAllIn(Exception):
    def __init__(self, player):
        self.player = player

class Pot(object):
    """
    Object to keep track of bets and decide the final splitting of money at
    the end of the round.
        
    The .bet method is used for each bet by a player, it will raise AlreadyAllIn
    if the player is betting after being all in and InsufficientBet if
    the bet by a player does not met or exceed the current bet level.
    
    The .total property can be used to get the current amount of money stored
    in the pot.
    """
    def __init__(self):
        self.current_bet = 0
        self.player_total = collections.defaultdict(int)
        self.all_in = {}
        
    @property
    def total(self):
        return sum(amount for amount in self.player_total.values())
    
    @staticmethod
    def subtract(player_totals, amount):
        """
        Subtract up to amount from each player's total, returning the
        total subtracted amount.
        """
        subtracted = 0
        player_totals = player_totals.copy()
        for player, player_total in player_totals.iteritems():
            if player_total > amount:
                subtracted += amount
                player_total -= amount
            else:
                subtracted += player_total
                player_total = 0
            player_totals[player] = player_total
        return player_totals, subtracted
        
    def bet(self, player, amount, all_in=False):
        """
        Bet some money.  Adds to the current total bet by a player.
        """
        self.player_total.setdefault(player, 0)
        player_bet = self.player_total[player] + amount
        if self.all_in.get(player, False):
            raise AlreadyAllIn(player)
        if all_in:
            self.all_in[player] = True
        else:
            if player_bet < self.current_bet:
                raise InsufficientBet(player, amount)
        # raise/call
        self.current_bet = player_bet
        self.player_total[player] = player_bet
        
    def get_winner_groups(self, ranking):
        """
        Convert the ranking into a list of groups of players who tied,
        in order of decreasing rank (so the players with the best hands are first)
        """
        hand_ranks = [hand_rank for hand_rank, player in ranking]
        for current_rank in reversed(sorted(set(hand_ranks))):
            yield [player for hand_rank, player in ranking if hand_rank == current_rank]
            
    def split_group(self, pots, winners):
        """
        For a group of people with equivalent hands, divide up whatever is
        left of the pot between them
        """
        pots = pots.copy()
        # default dict, all the players have won 0 credits by defaul
        winnings = collections.defaultdict(int)
        
        L = list(sorted((self.player_total[player], player) for player in winners))
        # at this point, the list is ordered so that the player with the lowest bet
        # goes first, and the pots that that player can get are split evenly
        # between all winners in this group
        while len(L) > 0:
            num_players = len(L)
            player_total, player = L[0]
            # get sum of pot totals that the player will get, remove any used 
            # pots from consideration as they are now empty
            pot_total = 0
            for key, total in pots.items():
                if key <= player_total:
                    pot_total += total
                    del pots[key]
            per_player_amount = pot_total / num_players
            extra = pot_total % num_players
            # split the winnings
            for _, player in L:
                winnings[player] += per_player_amount + extra
                extra = 0
            # remove the first player, he has got all the money he will get
            L = L[1:]
        return pots, winnings.items()
        
    def create_pots(self):
        """
        Create a dictionary of pots, indexed by the bet amount for each pot.
        If a player is all in, this creates a new pot with the amount that
        he is all in for as the bet amount.
        
        For each player that is all in, there is a pot, and possibly one more
        for the players that are not all in.
        """
        # default dict, all the pots have 0 credits by default
        pots = collections.defaultdict(int)
        # make a copy of the player_total dict for creating the pots
        # so that we don't modify the original
        player_total = self.player_total.copy()
        all_in_players = [(player_total[player], player) for player, all_in in self.all_in.iteritems() if all_in]
        for _, player in list(sorted(all_in_players)):
            player_total, pot_total = self.subtract(player_total, player_total[player])
            # index them according to the player's original final bet
            pots[self.player_total[player]] += pot_total
        # the remainder is a sort of final pot
        pots[self.current_bet] += sum(amount for amount in player_total.values())
        return pots

    def split(self, ranking):
        """
        A slightly complicated way of calculating who wins what based on the
        amount that each player has bet and their rankings vs other players.
        
        A ranking is a list of (hand_rank, player) pairs, it does not have
        to be ordered.
        """
        assert(len(ranking) > 0)
        pots = self.create_pots()
        total = self.total
        amount_distributed = 0
        for group in self.get_winner_groups(ranking):
            pots, winners = self.split_group(pots, group)
            for player, amount in winners:
                if amount > 0:
                    amount_distributed += amount
                    yield (player, amount)
        # this will be false if there is left over money in the pot,
        # for instance if you don't provide a complete ranking to the pot
        assert(amount_distributed == total)
                    
def doctest_pot():
    """
    Tests to make sure the pot splits correctly.
    
    Most basic pot:
    >>> pot = Pot()
    >>> pot.bet('p1', 10)
    >>> ranking = [(1, 'p1')]
    >>> print list(pot.split(ranking))
    [('p1', 10)]
    
    Pot goes to one player:
    >>> pot = Pot()
    >>> pot.bet('p1', 100)
    >>> pot.bet('p2', 100)
    >>> ranking = [(1, 'p1'), (2, 'p2')]
    >>> print list(pot.split(ranking))
    [('p2', 200)]
    
    Pot is split between two players:
    >>> pot = Pot()
    >>> pot.bet('p1', 100)
    >>> pot.bet('p2', 100)
    >>> ranking = [(1, 'p1'), (1, 'p2')]
    >>> print list(sorted(pot.split(ranking)))
    [('p1', 100), ('p2', 100)]
    
    >>> pot = Pot()
    >>> pot.bet('p1', 100, all_in=True)
    >>> pot.bet('p2', 100)
    >>> ranking = [(1, 'p1'), (1, 'p2')]
    >>> print list(sorted(pot.split(ranking)))
    [('p1', 100), ('p2', 100)]
    
    >>> pot = Pot()
    >>> pot.bet('p1', 100, all_in=True)
    >>> pot.bet('p2', 200)
    >>> ranking = [(1, 'p1'), (1, 'p2')]
    >>> print list(sorted(pot.split(ranking)))
    [('p1', 100), ('p2', 200)]
    
    >>> pot = Pot()
    >>> pot.bet('p1', 100)
    >>> pot.bet('p2', 100)
    >>> pot.bet('p3', 100)
    >>> ranking = [(1, 'p1'), (1, 'p2'), (2, 'p3')]
    >>> print list(sorted(pot.split(ranking)))
    [('p3', 300)]
    
    >>> pot = Pot()
    >>> pot.bet('p1', 100, all_in=True)
    >>> pot.bet('p2', 100)
    >>> pot.bet('p3', 100)
    >>> ranking = [(1, 'p1'), (1, 'p2'), (2, 'p3')]
    >>> print list(sorted(pot.split(ranking)))
    [('p3', 300)]
    
    >>> pot = Pot()
    >>> pot.bet('p1', 100)
    >>> pot.bet('p2', 100)
    >>> pot.bet('p3', 100)
    >>> ranking = [(2, 'p2'), (2, 'p3')]
    >>> print list(sorted(pot.split(ranking)))
    [('p2', 150), ('p3', 150)]
    
    >>> pot = Pot()
    >>> pot.bet('p1', 50, all_in=True)
    >>> pot.bet('p2', 80, all_in=True)
    >>> pot.bet('p3', 100)
    >>> pot.bet('p4', 100)
    >>> ranking = [(3, 'p1'), (2, 'p2'), (2, 'p3')]
    >>> print list(sorted(pot.split(ranking)))
    [('p1', 200), ('p2', 45), ('p3', 85)]
    
    >>> pot = Pot()
    >>> pot.bet('p1', 50, all_in=True)
    >>> pot.bet('p2', 50, all_in=True)
    >>> pot.bet('p3', 100)
    >>> pot.bet('p4', 100)
    >>> ranking = [(3, 'p1'), (3, 'p2'), (2, 'p3')]
    >>> print list(sorted(pot.split(ranking)))
    [('p1', 100), ('p2', 100), ('p3', 100)]
    
    Incomplete ranking, there is left over money that should go to either
    p3 or p4:
    >>> pot = Pot()
    >>> pot.bet('p1', 50, all_in=True)
    >>> pot.bet('p2', 50, all_in=True)
    >>> pot.bet('p3', 100)
    >>> pot.bet('p4', 100)
    >>> ranking = [(3, 'p1'), (3, 'p2')]
    >>> print list(sorted(pot.split(ranking)))
    Traceback (most recent call last):
        ...
    AssertionError
    
    >>> pot = Pot()
    >>> pot.bet('p1', 50, all_in=True)
    >>> pot.bet('p2', 80, all_in=True)
    >>> pot.bet('p3', 100)
    >>> pot.bet('p4', 100)
    >>> ranking = [(3, 'p1'), (2, 'p2'), (1, 'p3')]
    >>> print list(sorted(pot.split(ranking)))
    [('p1', 200), ('p2', 90), ('p3', 40)]
    
    >>> pot = Pot()
    >>> pot.bet('p1', 10)
    >>> pot.bet('p2', 10000, all_in=True)
    >>> pot.bet('p3', 10000, all_in=True)
    >>> ranking = [(1, 'p2'), (2, 'p3')]
    >>> print list(sorted(pot.split(ranking)))
    [('p3', 20010)]
    
    Highest players are all in:
    >>> pot = Pot()
    >>> pot.bet('p1', 10)
    >>> pot.bet('p2', 10000, all_in=True)
    >>> pot.bet('p3', 10010, all_in=True)
    >>> ranking = [(2, 'p2'), (1, 'p3')]
    >>> print list(sorted(pot.split(ranking)))
    [('p2', 20010), ('p3', 10)]
    """
    pass
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()