import random


class Unit:
    def __init__(self, ws, s, t, ap, sv, d, w):
        self.w = w
        self.d = d
        self.sv = sv
        self.ap = ap
        self.t = t
        self.s = s
        self.ws = ws
        
    @staticmethod
    def roll():
        roll = random.randint(1, 6)
        return roll
    
    def hit(self):
        roll = self.roll()
        return roll >= self.ws

    def wound(self, defender_t):
        roll = self.roll()
        if self.s >= defender_t * 2:
            required_roll = 2
        elif self.s > defender_t:
            required_roll = 3
        elif self.s == defender_t:
            required_roll = 4
        elif self.s <= defender_t / 2:
            required_roll = 6
        else:  # self.s < defender_t
            required_roll = 5
        return roll >= required_roll


def attack(attacker, defender):
    if attacker.hit():
        if attacker.wound(defender.t):
            return True
    return False


necron_warrior = Unit(ws=3, s=5, t=4, ap=-2, sv=4, d=1, w=1)
sm_intercessor = Unit(ws=3, s=4, t=4, ap=0, sv=3, d=1, w=2)


summ = 0
n = 10000
for i in range(0, n):
    summ += attack(necron_warrior, sm_intercessor)
print(summ / n)
