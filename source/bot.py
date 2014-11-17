from messages import Action

class Bot(object):
    def __init__(self, id, credits, big_blind_amount, small_blind_amount, *args, **kwargs):
        self.id = id
        self.initial_credits = credits
        self.credits = self.initial_credits
        self.big_blind_amount = big_blind_amount
        self.small_blind_amount = small_blind_amount
        self.event_queue = []
        
    def get_name(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return self.__class__.__name__
        
    def log(self, message):
        print '%s(%d): %s' % (self.get_name(), self.id, message)
        
    def action(self, type, amount=None):
        action = Action(type=type)
        if amount is not None:
            action.amount = amount
        return action
    
    def turn(self):
        raise NotImplementedError
        
    def __repr__(self):
        return "<%s player_id=%d>" % (self.get_name(), self.id)