from messages import Action

class BotWrapper(object):
    def __init__(self, bot, *args, **kwargs):
        self.id = kwargs['id']
        self.credits = kwargs['credits']
        self.bot = bot(*args, **kwargs)
        
    @staticmethod
    def filter_action(input_action):
        return input_action
        
    def turn(self):
        try:
            return self.bot.turn()
        except Exception, e:
            print "bot threw exception:",e
            return Action('fold')
            
    def __repr__(self):
        return self.bot.__repr__()