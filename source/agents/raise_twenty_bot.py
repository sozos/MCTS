from bot import Bot


class RaiseTwentyBot(Bot):
    def turn(self):
        return self.action('raise', amount=20)