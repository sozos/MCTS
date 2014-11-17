import random

from agents.mcts.uct import UCT
from helper_bot import HelperBot
from cards import n_card_rank

# Generate Cards Dictionary
cardsDict = [(r, s) for s in ['d', 'c', 'h', 's'] for r in range(2, 15)]


class PokerState:
    def __init__(self, hand, community_cards, a_credits, b_credits, curr_pot_diff, pot,
                a_invested, b_invested):
        self.credits = [a_credits, b_credits]
        self.hand = hand[:]
        self.community_cards = community_cards[:]
        self.playerJustMoved = 1 # At the root, pretend the player just moved is 1 (opp). Player 0 (us) has first move
        self.pot = pot
        self.invested = [a_invested, b_invested]
        self.opp_hand = None


        if curr_pot_diff == 0:
            self.moves_taken = []
        elif curr_pot_diff == 10:
            self.moves_taken = [1, 3]
        else:
            self.moves_taken = [1, 4]

    def clone(self):
        ps = PokerState(self.hand, self.community_cards, self.credits[0],
                        self.credits[1], self._get_pot_difference(), self.pot, self.invested[0],
                        self.invested[1])

        ps.playerJustMoved = self.playerJustMoved
        return ps

    def do_move(self, move):
        self.moves_taken += [move]
        player = self._get_player_turn()
        diff = self._get_pot_difference()

        if move == 1 or move == 2:
            self.credits[player] -= diff
            self.pot += diff
            self.invested[player] += diff
        elif move == 3:
            self.credits[player] -= (diff + 10)
            self.pot += (diff + 10)
            self.invested[player] += (diff + 10)
        elif move == 4:
            self.credits[player] -= (diff + 20)
            self.pot += (diff + 20)
            self.invested[player] += (diff + 10)

        self.playerJustMoved = (self.playerJustMoved + 1) % 2

    def get_moves(self):
        if self._get_folded() != -1 or self._get_stage_num() == 5:
            return []
        # if self.playerJustMoved == 0:
        #     return [4]

        player = self._get_player_turn()
        diff = self._get_pot_difference()
        
        moves = [0]
        if diff == 0:
            moves += [1]
        
        if self.credits[(player + 1) % 2] == 0:
            return moves

        if self.credits[player] >= diff:
            moves += [2]

        if self.credits[player] >= diff + 10:
            moves += [3]

        if self.credits[player] >= diff + 20:
            moves += [4]
            
        return moves

    # def get_result(self, playerjm):
    #     if self._get_folded() == playerjm:
    #         return -self.invested[playerjm]  # 0
    #     elif self._get_folded() == (playerjm + 1) % 2:
    #         return self.pot - self.invested[playerjm]
    #     else:
    #         # evaluate
    #         if self.opp_hand is None:
    #             self.opp_hand = []
    #             while len(self.opp_hand) < 2:
    #                 c = cardsDict[random.randrange(52)]
    #                 if not c in self.hand + self.community_cards + self.opp_hand:
    #                     self.opp_hand += [c]
    #         while len(self.community_cards) < 5:
    #             c = cardsDict[random.randrange(52)]
    #             if not c in self.hand + self.community_cards + self.opp_hand:
    #                 self.community_cards += [c]
    #
    #         player_0 = n_card_rank(self.hand + self.community_cards)
    #         player_2 = n_card_rank(self.opp_hand + self.community_cards)
    #         if player_0 == max(player_0, player_2):
    #             return self.pot - self.invested[playerjm] if playerjm == 0 else -self.invested[playerjm]  #
    #         else:
    #             # return -self.invested[playerjm] if playerjm == 0 else self.pot - self.invested[playerjm]
    def get_result(self, playerjm):
        total_chips = 2000.0
        if self._get_folded() == playerjm:
            return 0  # -self.invested[playerjm]  # 0
        elif self._get_folded() == (playerjm + 1) % 2:
            return (self.pot - self.invested[playerjm]) / total_chips
        else:
            # evaluate
            if self.opp_hand is None:
                self.opp_hand = []
                while len(self.opp_hand) < 2:
                    c = cardsDict[random.randrange(52)]
                    if not c in self.hand + self.community_cards + self.opp_hand:
                        self.opp_hand += [c]
            while len(self.community_cards) < 5:
                c = cardsDict[random.randrange(52)]
                if not c in self.hand + self.community_cards + self.opp_hand:
                    self.community_cards += [c]

            player_0 = n_card_rank(self.hand + self.community_cards)
            player_2 = n_card_rank(self.opp_hand + self.community_cards)
            if player_0 == max(player_0, player_2):
                return (self.pot - self.invested[playerjm]) / total_chips if playerjm == 0 else 0  # -self.invested[playerjm]  #
            else:
                return 0 if playerjm == 0 else (self.pot - self.invested[playerjm]) / total_chips

    def _get_player_turn(self):
        return len(self.moves_taken) % 2

    def _get_folded(self):
        if len(self.moves_taken) == 0 or self.moves_taken[-1] != 0:
            return -1
        else:
            return (len(self.moves_taken) + 1) % 2

    def _get_pot_difference(self):
        sums = [0, 0]

        for i in range(1, len(self.moves_taken) + 1):
            if self.moves_taken[-i] == 3:
                sums[-i % 2] += 10
            elif self.moves_taken[-i] == 4:
                sums[-i % 2] += 20
            else:
                pass
        return abs(sums[0] - sums[1])

    def _get_stage_num(self):
        num = 0
        consecutive_check = 0

        for move in self.moves_taken:
            if move == 1:
                if consecutive_check == 1:
                    num += 1
                    consecutive_check = 0
                else:
                    consecutive_check = 1
            else:
                consecutive_check = 0
                if move == 2:
                    num += 1

        return num


class MctsBot(HelperBot):
    def turn(self):
        self._process_events()
        state = PokerState(self.hand, self.community_cards, self.credits,
                           self.opponent[1], self.pot_diff, self.pot, self.invested[self.player_id],
                           self.invested[(self.player_id + 1) % 2])

        m = UCT(rootstate=state, itermax=1000, verbose=False)
        action_names = ['fold', 'check', 'call', 'raise 10', 'raise 20']
        action_list = [self.action('fold'), self.action('check'),
                       self.action('call'), self.action('raise', 10),
                       self.action('raise', 20)]

        print("Player %d %s" % (self.player_id, action_names[m]))
        # if m == 0:
        #     print self.hand
        return action_list[m]

    def _process_events(self):
        for event in self.event_queue:
            method_name = '_' + event.type
            method = getattr(self, method_name)
            if not method:
                raise Exception("Method %s not implemented" % method_name)
            method(event)

        self.event_queue = []

    def _join(self, event):
        self.player_id = (event.player_id + 1) % 2
        self.opponent = [event.player_id, event.credits]

    def _new_round(self, event):
        self.community_cards = []
        self.pot = 0
        self.pot_diff = 0
        self.invested = [0, 0]

    def _button(self, event):
        self.button = self.player_id == event.player_id

    def _deal(self, event):
        self.round = "deal"
        self.hand = event.cards[:]
        # self.hand = [(14, 's'), (14, 'h')]
        # print self.hand

    def _flop(self, event):
        self.round = "flop"
        self.community_cards += event.cards

    def _turn(self, event):
        self.round = "turn"
        self.community_cards += [event.card]

    def _river(self, event):
        self.round = "river"
        self.community_cards += [event.card]

    def _action(self, event):
        if event.action.type == 'call':
            self.pot += self.pot_diff
            player = event.player_id
            self.invested[player] += self.pot_diff
            self.pot_diff = 0
        elif event.action.type == 'raise':
            self.pot += (self.pot_diff + event.action.amount)
            player = event.player_id
            self.invested[player] += (self.pot_diff + event.action.amount)
            self.pot_diff = event.action.amount

    def _adjust_credits(self, event):
        if event.player_id == self.player_id:
            self.credits += event.amount
        else:
            self.opponent[1] += event.amount

    def _big_blind(self, event):
        self.pot += 20

    def _small_blind(self, event):
        self.pot_diff = 10
        self.pot += 10

    def _win(self, event):
        pass

    def _bad_bot(self, event):
        pass

    def _end_of_round(self, event):
        pass
