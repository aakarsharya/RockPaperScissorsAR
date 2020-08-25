import time
import random
import string
from player import Player

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
            'players': [player.to_json() for player in self.players]
        }
            
    def addPlayer(self, player_id):
        self.players.append(Player(player_id))
        self.numPlayers += 1

    def getPlayer(self, sid):
        for player in self.players:
            if player.sid == sid:
                return player

    def containsPlayer(self, sid):
        for player in self.players:
            if player.sid == sid:
                return True
        return False

    def removePlayer(self, sid):
        self.players.remove(sid)
        self.numPlayers -= 1

    def isReady(self):
        if self.numPlayers < 2:
            return False

        allPlayersReady = True
        for player in self.players:
            if player.isReady() == False:
                allPlayersReady = False
        
        return allPlayersReady

    def unready(self):
        for player in self.players:
            player.unready()

    def computeWinner(self):
        p1 = self.players[0]
        p2 = self.players[1]
        result = {}

        if p1.hand == 'other' or p2.hand == 'other' or p1.hand == p2.hand:
            result = {p1.sid: {'result': 'tie'}, p2.sid: {'result': 'tie'}}
        elif p1.hand == 'rock':
            if p2.hand == 'paper':
                result = {p1.sid: {'result': 'loss'}, p2.sid: {'result': 'win'}}
            else:
                result = {p1.sid: {'result': 'win'}, p2.sid: {'result': 'loss'}}
        elif p1.hand == 'paper':
            if p2.hand == 'rock':
                result = {p1.sid: {'result': 'win'}, p2.sid: {'result': 'loss'}}
            else:
                result = {p1.sid: {'result': 'loss'}, p2.sid: {'result': 'win'}}
        else:
            if p2.hand == 'paper':
                result = {p1.sid: {'result': 'win'}, p2.sid: {'result': 'loss'}}
            else:
                result = {p1.sid: {'result': 'loss'}, p2.sid: {'result': 'win'}}
        
        return result

    def play(self):
        result = self.computeWinner()
        
        for player in self.players:
            result[player.sid]['img'] = player.img
            result[player.sid]['hand'] = player.hand

        self.unready()
        return result

            

