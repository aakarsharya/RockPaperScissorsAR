import time
import random
import string

HANDS = ['rock', 'paper', 'scissors']

class Game(object):
    def __init__(self):
        self.game_id = self.generate_room_id()
        self.players = []
        self.numPlayers = 0

    @classmethod
    def generate_room_id(cls):
        """Generate a random room ID"""
        id_length = 5
        return ''.join(random.SystemRandom().choice(
            string.ascii_uppercase) for _ in range(id_length))

    def to_json(self):
        return {
            'game_id': self.game_id,
            'players': self.players
        }
            
    def addPlayer(self, player_id):
        self.players.append(player_id)
        self.numPlayers += 1

    def getPlayer(self, sid):
        for player in self.players:
            if player.id == sid:
                return player

    def removePlayer(self, sid):
        self.players.remove(sid)
        self.numPlayers -= 1
