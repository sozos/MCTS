from helper_bot import HelperBot

class HumanBot(HelperBot):
    def turn(self):
        print "Community Cards: " + str(self.get_community_cards())
        print "Hand: " + str(self.get_hand())

        action = raw_input('Action: ').split()
        if action[0] == 'raise':
            return self.action('raise', amount=int(action[1]))
        elif action[0] == 'check' or action[0] == 'call':
            return self.action(action[0])
        else:
            return self.action('fold')