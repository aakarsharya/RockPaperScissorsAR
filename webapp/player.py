import time

class Player(object):
    def __init__(self, sid):
        self.hand = 'other'
        self.sid = sid
        self.ready = False
        self.img = None

    def to_json(self):
        return {
            'hand': self.hand,
            'sid': self.sid,
            'ready': self.ready
        }
    
    def updateHand(self, hand, img):
        self.hand = hand
        self.ready = True
        self.img = img

    def unready(self):
        self.ready = False

    def isReady(self):
        return self.ready
