"""

proto_bot

A bot that actually runs a command-line program and interfaces with it over
stdin and stdout. Messages are passed using Google Protocol Buffers. Protocol
Buffers supports C++ and Java, so making programs in either of these languages
should be quite doable.

If you want output from your program, set output_stderr to True. It will be
mixed in with the python output though. Writing to your own file would be a
another method, or else redirect stderr to a file using "2> file.txt".

For an example on how to use this, see example_bots/proto_bot. The wiki
contains a protocol reference, and the .proto file is at
protocol/poker_bot.proto.

"""

from subprocess import Popen, PIPE, STDOUT
import os
import sys

# add the protobuf libraries to the python path
path = os.path.join(os.path.dirname(__file__), 'protocol/python/lib')
sys.path.append(os.path.abspath(path))

import protocol.python.protocol.poker_bot_pb2 as protocol
import protocol.python.lib.poker_messaging as messaging

from messages import Event, Action
from bot import Bot

# process control functions, not available on windows
import platform
if platform.system() == 'Windows':
    def stop_process(p):
        pass

    def continue_process(p):
        pass
else:
    import signal
    def stop_process(p):
        os.kill(p.pid, signal.SIGSTOP)

    def continue_process(p):
        os.kill(p.pid, signal.SIGCONT)

# conversion functions
def card_to_pbcard(card, pb_card):
    # modifies passed in pb_card
    value, suit = card
    pb_card.value = value
    full_suit = {
        'h': 'HEARTS',
        'd': 'DIAMONDS',
        's': 'SPADES',
        'c': 'CLUBS',
    }[suit]
    pb_card.suit = getattr(protocol.Event.Card, full_suit)
    
def event_to_pbevent(event):
    """
    Convert an Event object into a Protocol Buffer Event.
    """
    pb_event = protocol.Event()
    # any properties that the event object has need to be set on
    # the protocol_event
    keys = [key for key in dir(event) if not key.startswith('_') and key not in ['type', 'cards', 'action', 'card']]
    for key in keys:
        value = getattr(event, key)
        if key in ['amount', 'credits']:
            value = int(value)
        setattr(pb_event, key, value)
    # set type
    if hasattr(protocol.Event, event.type.upper()):
        pb_event.type = getattr(protocol.Event, event.type.upper())
    else:
        print "ERROR: could not convert event type '%s'" % event.type.upper()
    # set cards, if applicable
    if hasattr(event, 'cards'):
        for card in event.cards:
            pb_card = pb_event.cards.add()
            card_to_pbcard(card, pb_card)
    # set card, if applicable
    if hasattr(event, 'card'):
        card_to_pbcard(event.card, pb_event.card)
    # set action, if applicable
    if hasattr(event, 'action'):
        pb_event.action.CopyFrom(action_to_pb_action(event.action))
    return pb_event
    
def action_to_pb_action(action):
    """
    Convert an Action object into a Protocol Buffer Action.
    """
    pb_action = protocol.Action()
    # set type
    pb_action.type = getattr(protocol.Action, action.type.upper())
    # set amount if applicable
    if hasattr(action, 'amount'):
        pb_action.amount = int(action.amount)
    return pb_action
    
def pb_action_to_action(pb_action):
    """
    Convert a Protocol Buffer Action into an Action object.
    """
    action = Action(type='fold')
    keys = [key for key in dir(protocol.Action) if key.isupper()]
    for key in keys:
        if getattr(protocol.Action, key) == pb_action.type:
            action.type = key.lower()
            break
    else:
        raise Exception("Could not decode action type %d" % pb_action.type)
    if hasattr(pb_action, 'amount'):
        action.amount = pb_action.amount
    return action


class ProtoBot(Bot):
    output_stderr = False
    def __init__(self, *args, **kwargs):
        """
        Create a new ProtoBot, expects the self.executable to be set in a
        subclass.  This is the path to an executable that speaks the proper
        protocol over stdin and stdout.
        """
        super(ProtoBot, self).__init__(*args, **kwargs)
        if not hasattr(self, 'command'):
            raise Exception("You must subclass ProtoBot and set the 'command' attribute")
        # spawn the process
        cmd = self.command + \
                [
                    'credits:%d' % self.initial_credits,
                    'id:%d' % self.id,
                    'small_blind_amount:%d' % self.small_blind_amount,
                    'big_blind_amount:%d' % self.big_blind_amount,
                ]
        print "Running ProtoBot %s" % cmd
        if self.output_stderr:
            self.stderr = None
        else:
            self.stderr = PIPE
        self.p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=self.stderr)
        # stdin/stdout are now self.p.stdin/stdout
        
    def __del__(self):
        """
        Close the child process
        """
        if hasattr(self, 'p'):
            messaging.send_terminator(self.p.stdin)
        
    def send_event(self, event):
        """
        Send the specified Event object to the child process' stdin
        """
        pb_event = event_to_pbevent(event)
        messaging.send_message(self.p.stdin, pb_event)
        
    def receive_action(self):
        """
        Get an Action object from the child process' stdout
        """
        pb_action = messaging.receive_message(self.p.stdout, protocol.Action)
        return pb_action_to_action(pb_action)
        
    def turn(self):
        """
        Send all events to the bot and then get the bot's action
        """
        self.log("bot's turn")
        continue_process(self.p)
        # write the events to the child, then tell the child that it is
        # his turn
        self.log("sending events to bot")
        for event in self.event_queue:
            self.send_event(event)
        self.event_queue = []
            
        self.send_event(Event(type='your_turn'))
        
        self.log("waiting for response from bot")
        # get the action produced by the bot
        action = self.receive_action()
        self.log("got response from bot")
        stop_process(self.p)
        self.log("end of bot's turn")
        return action
            