import os
this_dir = os.path.dirname(os.path.realpath( __file__ ))

from proto_bot import ProtoBot

class FoldBotJava(ProtoBot):
    command = ['java', '-jar', os.path.join(this_dir, 'foldbot/dist/foldbot.jar')]
    output_stderr = True
