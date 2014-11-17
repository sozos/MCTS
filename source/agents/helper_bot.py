from bot import Bot

class HelperBot(Bot):
    def __init__(self, id, credits, big_blind_amount, small_blind_amount, *args, **kwargs):
        super(HelperBot, self).__init__(id, credits, big_blind_amount, small_blind_amount, *args, **kwargs)
        self.hand = []
        self.community_cards = []

    def get_rank(card):
        return card[0]

    def get_suit(card):
        return card[1]

    def get_hand(self):
        hand = []
        for event in self.event_queue:
            if event.type == 'deal':
                hand = event.cards
        self.hand = hand
        return hand

    def update_community_cards(self):
        community_cards = []
        for event in self.event_queue:
            if event.type == 'new_round':
                community_cards = []
            if (event.type == 'flop' or
                event.type == 'turn' or
                event.type == 'river'):
                    try:
                        community_cards += event.cards
                    except AttributeError:
                        community_cards += [event.card]
        self.community_cards = community_cards

    def get_community_cards(self):
        self.update_community_cards()
        return self.community_cards

    def get_game_turn(self):
        num_community_cards = len(self.get_community_cards())
        if num_community_cards == 0:
            # Deal
            print "Deal"
            return 0
        elif num_community_cards == 3:
            # Flop
            print "Flop"
            return 1
        elif num_community_cards == 4:
            # Turn
            print "Turn"
            return 2
        elif num_community_cards == 5:
            # River
            print "River"
            return 3
        else:
            # Error
            return -1