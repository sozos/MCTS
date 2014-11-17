from bot import Bot
from messages import Action

class FoldBot(Bot):
    def turn(self):
        self.log("my turn")
        self.log("%d events in queue" % len(self.event_queue))
        self.event_queue = []
        return self.action('fold')