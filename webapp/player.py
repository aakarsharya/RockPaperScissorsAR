import time

class Player(object):
    def __init__(self, sid):
        self.game_history = {'wins': 0, 'losses': 0, 'ties': 0}
        self.hand = 'other'
        self.id = sid

    def updateScore(self, score: str):
        self.game_history[score] += 1
