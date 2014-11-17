import random
import copy
import logging
import collections

from cards import Deck, n_card_rank
from messages import Event, Action
from pot import Pot
from bot_wrapper import BotWrapper

# TODO: correct handling of heads_up -> button selection etc
# TODO: logging module
# TODO: player wrapper with credits, id, __str__ etc, move action sanitizing into there
# TODO: less retarded example bot
# TODO: more docs

class WinByDefault(Exception):
    def __init__(self, winner):
        self.winner = winner

class PokerGame(object):
    def __init__(self, bots, initial_credits=1000, num_decks=1,
            small_blind_amount=10, seed=None):
        self.players = []
        self.credits = {}
        self.id = {}
        self.deck = Deck()
        # big blind amount is 2x small_blind_amount
        self.small_blind_amount = small_blind_amount
        
        # initialize randomness
        if seed is None:
            random.seed() # seed with, hopefully, /dev/urandom
            seed = random.randint(0, 2**32)
        self.output("random seed: %d" % seed)
        random.seed(seed)
        
        for id, bot in enumerate(bots):
            bot_instance = bot(id=id, credits=initial_credits, small_blind_amount=self.small_blind_amount, big_blind_amount=self.big_blind_amount)
            self.players.append(bot_instance)
            self.id[bot_instance] = id
            self.credits[bot_instance] = initial_credits
        self.active_players = copy.copy(self.players)
        
    @property
    def big_blind_amount(self):
        return self.small_blind_amount * 2

    def run(self):
        assert(len(self.active_players) > 0)
        
        round_num = 1
        # button is random and goes to the next player (higher index) each round,
        # looping around at the end
        button = random.choice(self.active_players)
        
        # send out join messages
        for player in self.active_players:
            for other_player in self.active_players:
                if player is not other_player:
                    event = Event('join', player_id=self.id[player], credits=self.credits[player])
                    self.send_event(other_player, event)
        
        self.output("Start of Game State:")
        self.print_state()
                        
        while len(self.active_players) > 1:
            self.broadcast_event(Event('new_round'))
            self.output("Round: %d" % round_num)
            round = Round(self, button)
            round.run()
            self.output("End of Round State:")
            self.print_state()
            self.broadcast_event(Event('end_of_round'))
            round_num += 1
            
            button = self.active_players[(self.active_players.index(button)+1) % len(self.active_players)]
            # determine next blinds, remove any players that are at 0 credits
            # or can't pay the blind
            button = self.remove_losers(button)
            
        self.output("Game Over")
        winner = self.active_players[0]
        self.output("Game Winner: %s with credits %d" % (winner, self.credits[winner]))
        return (winner, self.credits[winner])
            
    def print_state(self):
        for player in self.active_players:
            self.output("\t%s with credits %d" % (player, self.credits[player]))
            
    def remove_losers(self, button):
        # find anyone with no money
        for player in self.active_players:
            if self.credits[player] <= 0:
                if player == button:
                    # figure out next button
                    i = self.active_players.index(player)
                    button_index = (i+1) % len(self.active_players)
                    button = self.active_players[button_index]
                self.remove_loser(player)
        return button
    
    def broadcast_event(self, event):
        # self.output("Broadcast Event: %s" % event)

        if event.type == 'button':
            self.output("Player %d has the button" % event.player_id)
        if event.type == 'flop':
            self.output("Flop: %s" % event.cards)
        if event.type == 'turn':
            self.output("Turn: %s" % str(event.card))
        if event.type == 'river':
            self.output("River: %s" % str(event.card))
        if event.type == 'win':
            self.output('Player %d wins!' % event.player_id)

        for player in self.active_players:
            player.event_queue.append(event)
            
    def send_event(self, player, event):
        # self.output("Event to player %d: %s" % (self.id[player], event))
        player.event_queue.append(event)
            
    def remove_loser(self, player):
        self.active_players.remove(player)
        self.broadcast_event(Event('quit', player_id=self.id[player]))
        
    def adjust_credits(self, player, amount):
        self.credits[player] += amount
        self.broadcast_event(Event('adjust_credits', player_id=self.id[player], amount=amount))
    
    def output(self, msg):
        print "Dealer: %s" % msg
        
class Round(object):
    def __init__(self, game, button):
        self.game = game
        # make a copy of the deck for this round and shuffle it
        self.deck = copy.copy(game.deck)
        self.deck.shuffle()
        self.players = copy.copy(game.active_players)
        self.active_players = copy.copy(self.players)
        self.button = button
        self.pot = Pot()
        self.all_in = []
        
    def run(self):
        self.game.broadcast_event(Event('button', player_id=self.game.id[self.button]))
        # do the blinds
        small_blind, big_blind = self.calculate_blinds(self.button)
        # self.game.broadcast_event(Event('small_blind', player_id=self.game.id[small_blind]))
        self.bet(small_blind, self.game.small_blind_amount)
        # self.game.broadcast_event(Event('big_blind', player_id=self.game.id[big_blind]))
        self.bet(big_blind, self.game.big_blind_amount)
        
        hole_cards = {}
        # deal each player 2 cards
        for player in self.players:
            hole_cards[player] = self.deck.take(2)
            self.game.send_event(player, Event('deal', cards=copy.copy(hole_cards[player])))
        
        try:
            # first round of betting, no 'check' allowed unless you're the big
            # blind and nobody raised
            self.betting_round(1, self.button, self.pot)
        
            # flop
            community_cards = self.deck.take(3)
            self.game.broadcast_event(Event('flop', cards=copy.copy(community_cards)))
        
            self.betting_round(2, self.button, self.pot)
        
            # turn
            turn = self.deck.take_one()
            self.game.broadcast_event(Event('turn', card=turn))
            community_cards.append(turn)
        
            self.betting_round(3, self.button, self.pot)
        
            # river
            river = self.deck.take_one()
            self.game.broadcast_event(Event('river', card=river))
            community_cards.append(river)
        
            # final betting round
            self.betting_round(4, self.button, self.pot)
        except WinByDefault, e:
            player = e.winner
            credits = self.pot.total
            # TODO: win should indicate amount won, (gained over previous round)
            self.game.broadcast_event(Event('win', player_id=self.game.id[player], rank=0, amount=credits))
            self.game.adjust_credits(player, credits)
        else:
            ranking = self.determine_ranking(community_cards, hole_cards)
            for rank, (player, credits) in enumerate(reversed(sorted(self.pot.split(ranking)))):
                self.game.broadcast_event(Event('win', player_id=self.game.id[player], rank=rank, amount=credits))
                self.game.adjust_credits(player, credits)
                
    def run_turn(self, player):
        try:
            return player.turn()
        except Exception, e:
            self.game.send_event(player, Event('bad_bot', message='bot threw an exception: ' + str(e), action=None))
            return Action('fold')
            
    def get_player(self, index):
        return self.players[index % len(self.players)]
            
    def calculate_blinds(self, button):
        i = self.players.index(button)
        if len(self.players) == 2:
            small_blind = button
            big_blind = self.get_player(i+1)
        else:
            small_blind = self.get_player(i+1)
            big_blind = self.get_player(i+2)
        return small_blind, big_blind
        
    def bet(self, player, amount):
        assert(player not in self.all_in)
        if self.game.credits[player] <= amount:
            amount = self.game.credits[player]
            self.all_in.append(player)
        # if the player is all in, indicate that to the pot
        all_in = player in self.all_in
        self.pot.bet(player, amount, all_in)
        self.game.adjust_credits(player, -amount)
        
    def next_player(self, player):
        return self.get_player(self.players.index(player)+1)
        
    def betting_round(self, n, button, pot):
        player_bets = {}
        self.has_bet = {}
        # TODO: don't let player keep betting if it's just him and all_in guys
        for player in self.players:
            player_bets[player] = 0
            
        small_blind, big_blind = self.calculate_blinds(button)
        if n == 1:
            current_player = self.get_player(self.players.index(big_blind) + 1)
            player_bets[small_blind] = self.game.small_blind_amount
            player_bets[big_blind] = self.game.big_blind_amount
            current_bet = self.game.big_blind_amount
        else:
            current_player = self.get_player(self.players.index(button) + 1)
            current_bet = 0
             
        self.game.output("Start of betting round %d" % n)
            
        while True:
            if len(self.active_players) == 1:
                winner = self.active_players[0]
                self.game.output("Player %s won when everyone else folded" % winner)
                raise WinByDefault(winner)
                
            # figure out if this betting round is over
            for player in self.active_players:
                if player not in self.has_bet and player not in self.all_in:
                    break # found a player that can still make an action
            else:
                break # all players have bet, folded, or are all in, break out of the while loop
                
            # if player is all in, he does not get another turn
            if current_player in self.all_in:
                self.game.output("Player is all in, skipping %s" % current_player)
                current_player = self.next_player(current_player)
                continue
                
            if current_player not in self.active_players:
                self.game.output("Player has folded, skipping %s" % current_player)
                current_player = self.next_player(current_player)
                continue
            
            action = self.run_turn(current_player)
            def warn(message):
                self.game.send_event(current_player, Event('bad_bot', message=message, action=action))
                
            if action is None or \
                  getattr(action, 'type', None) not in ['fold', 'call', 'raise', 'check'] or \
                  action.type == 'raise' and not hasattr(action, 'amount'):
                warn('invalid action, folding')
                action = Action('fold')
                    
            if action.type == 'raise':
                if action.amount <=0 or self.game.credits[current_player] < action.amount:
                    warn('invalid raise, calling')
                    action = Action('call')
                else:
                    amount_to_bet = action.amount + (current_bet - player_bets[current_player])
                    if self.game.credits[current_player] < amount_to_bet:
                        warn('tried to raise more than player possesses, betting maximum')
                        amount_to_bet = self.game.credits[current_player]
                    if player_bets[current_player] + amount_to_bet > current_bet:
                        current_bet = player_bets[current_player] + amount_to_bet
                    self.bet(current_player, amount_to_bet)
                    player_bets[current_player] += amount_to_bet
                    self.has_bet = {current_player: True}
                    
            if action.type == 'call':
                if current_bet == 0:
                    warn('tried to call on zero bet, checking')
                    action = Action('check')
                elif current_bet == player_bets[current_player]:
                    warn('tried to call but had already bet that amount, should have checked, checking')
                    action = Action('check')
                else:
                    amount_to_bet = current_bet-player_bets[current_player]
                    self.bet(current_player, amount_to_bet)
                    player_bets[current_player] += amount_to_bet
                    self.has_bet[current_player] = True
                    
            if action.type == 'check':
                if current_bet != player_bets[current_player]:
                    warn('tried to check when not up to current bet, calling')
                    # TODO: action = Action('call')
                    amount_to_bet = current_bet-player_bets[current_player]
                    self.bet(current_player, amount_to_bet)
                    player_bets[current_player] += amount_to_bet
                    self.has_bet[current_player] = True
                else:
                    self.has_bet[current_player] = True
                
            if action.type == 'fold':
                self.active_players.remove(current_player)
                
            self.game.broadcast_event(Event('action', action=action, player_id=self.game.id[current_player]))
            current_player = self.next_player(current_player)
            
        self.game.output("End of betting round %d" % n)
            
    def determine_ranking(self, community_cards, hole_cards):
        # determine the best hand for each player
        hand_ranks = []
        for player in self.active_players:
            cards = community_cards + hole_cards[player]
            hand_rank = n_card_rank(cards)
            self.game.output("Player: %s with %s using cards %s" % (player, hand_rank, cards))
            hand_ranks.append((hand_rank, player))
        return hand_ranks