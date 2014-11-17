import os
import platform

this_dir = os.path.dirname(os.path.realpath( __file__ ))

from proto_bot import ProtoBot

class FoldBotCpp(ProtoBot):
    if platform.system() == 'Windows':
        command = [os.path.join(this_dir, 'foldbot/foldbot.exe')]
    else:
        command = [os.path.join(this_dir, 'foldbot/foldbot')]
    output_stderr = True