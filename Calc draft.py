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
        return random.randint(1, 6)
    
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
            return defender.sv > defender.roll() - attacker.ap
    return False


def damage_chance(attacker, defender):
    summ = 0
    n = 10000
    for i in range(0, n):
        summ += attack(attacker, defender)
    return summ / n


def mean_hit_qty(n, p):
    print(n * p - (1 - p))
    print(n * p + p)


necron_warrior_reaper = Unit(ws=3, s=5, t=4, ap=2, sv=4, d=1, w=1)
sm_intercessor = Unit(ws=3, s=5, t=4, ap=2, sv=4, d=1, w=1)
# chance = damage_chance(necron_warrior_reaper, sm_intercessor)
# mean_hit_qty(20, chance)

necron_warrior_flayer = Unit(ws=3, s=4, t=4, ap=1, sv=4, d=1, w=1)
# chance = damage_chance(necron_warrior_flayer, sm_intercessor)
# mean_hit_qty(20, chance)


necron_immortal_gauss = Unit(ws=3, s=5, t=5, ap=2, sv=3, d=1, w=1)
chance = damage_chance(necron_immortal_gauss, sm_intercessor)
mean_hit_qty(10, chance)

necron_immortal_tesla = Unit(ws=3, s=5, t=5, ap=0, sv=3, d=1, w=1)
chance = damage_chance(necron_immortal_tesla, sm_intercessor)
mean_hit_qty(13, chance)

mean_hit_qty(10, 1/6)
