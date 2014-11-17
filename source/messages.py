"""

Only two types of messages, Events, sent to the bot from the dealer, and
Actions, sent to the dealer from the bot.

Action format:
.type <properties>
'fold',
   fold means you quit this round
'call', 
   call means you match the current high bet
'raise' amount=number
   raise means you match the current high bet and add some amount to it
'check' (not available on first round, except for the big blind)
   a check is just a pass

Event format:
.type <properties>
'join' player_id=number credits=number
'new_round'
'button' player_id=number
'big_blind' player_id=number
'small_blind' player_id=number
'deal' cards
'flop' cards
'turn' card
    fourth community card
'river' card
    fifth community card
'action' player_id=number action=Action
'adjust_credits'  player_id=number amount=number (positive or negative)
'win' player_id=number rank=number amount=number
    there is also an adjust_credits event for this
    in the case that there are multiple winners
    the rank will indicate who won first, second etc (int, starts at zero)
    TODO: amount here should be amount won vs beginning of round
'end_of_round'
'quit' player_id=number
'bad_bot' message=string action=Action
    last action by your bot was determined to be invalid
    
card := (value, 'suit') where value is 2-14 and suit is one of ['d', 'h', 's', 'c']
cards := [card, card, ...]

"""

class KeywordObject(object):
    def __init__(self, type, **kwargs):
        self.type = type
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
        #print "created: %s" % self.__str__()
            
    def __str__(self):
        result = "<%s type=%s%s>"
        attributes = ""
        for k,v in sorted(self.__dict__.iteritems()):
            if k.startswith('_') or k == 'type':
                continue
            attributes += " %s=%s" % (k, v)
        return result % (self.__class__.__name__, self.type, attributes)

# 
class Event(KeywordObject):
    pass
        
class Action(KeywordObject):
    pass