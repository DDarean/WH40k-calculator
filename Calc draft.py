import random


class Unit:
    def __init__(self, weapon, ws, s, t, sv, w):
        self.w = w
        self.d = weapon.d
        self.sv = sv
        self.ap = weapon.ap
        self.t = t
        if weapon.s == 'User':
            self.s = s
        else:
            self.s = weapon.s
        self.ws = ws
        self.num_of_shots = weapon.num_of_shots

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
        else:  # self.weapon_s < defender_t
            required_roll = 5
        return roll >= required_roll


class Weapon:
    def __init__(self, name, s, ap, d, w_type, num_of_shots):
        self.num_of_shots = num_of_shots
        self.w_type = w_type
        self.d = d
        self.ap = ap
        self.s = s
        self.name = name


class Shooting:
    def __init__(self, attacker, defender):
        self.defender = defender
        self.attacker = attacker

    def attack(self):
        if self.attacker.hit():
            if self.attacker.wound(self.defender.t):
                return self.defender.sv > \
                       self.defender.roll() - self.attacker.ap
        return False

    def damage_chance(self, n=100000):
        summ = 0
        for i in range(0, n):
            summ += self.attack()
        return summ / n

    def mean_wound_qty(self, n=10):
        p = self.damage_chance()
        low = round(n * p - (1 - p), 2)
        high = round(n * p + p, 2)
        return (low + high) / 2

    def mean_damage(self, n=10):
        return self.mean_wound_qty(n) * self.attacker.num_of_shots


gauss_flayer = Weapon('Gauss flayer', s=4, ap=1, d=1,
                      w_type='Rapid fire', num_of_shots=1)
gauss_reaper = Weapon('Gauss reaper', s=5, ap=2, d=1,
                      w_type='Assault', num_of_shots=2)
bolt_pistol = Weapon('Bolt pistol', s=4, ap=0, d=1,
                     w_type='Pistol', num_of_shots=1)

sm_intercessor = Unit(bolt_pistol, ws=3, s=4, t=4, sv=3, w=2)
necron_warrior_reaper = Unit(gauss_reaper, ws=3, s=4, t=4, sv=4, w=1)
necron_warrior_flayer = Unit(gauss_flayer, ws=3, s=4, t=4, sv=4, w=1)

battle = Shooting(necron_warrior_reaper, sm_intercessor)
# print(battle.mean_wound_qty(n=20))
print(battle.mean_damage(n=10))
battle = Shooting(necron_warrior_flayer, sm_intercessor)
# print(battle.mean_wound_qty(n=20))
print(battle.mean_damage(n=10))
"""
chance = damage_chance(necron_warrior_reaper, sm_intercessor)
wound = mean_wound_qty(20, chance)
print(wound)
print(mean_damage(wound, 1))
chance = damage_chance(necron_warrior_flayer, sm_intercessor)
wound = mean_wound_qty(20, chance)
print(wound)
print(mean_damage(wound, 1))
"""
"""
necron_immortal_gauss = Unit(ws=3, s=5, t=5, ap=2, sv=3, d=1, w=1)
chance = damage_chance(necron_immortal_gauss, sm_intercessor)
mean_hit_qty(10, chance)

necron_immortal_tesla = Unit(ws=3, s=5, t=5, ap=0, sv=3, d=1, w=1)
chance = damage_chance(necron_immortal_tesla, sm_intercessor)
mean_hit_qty(13, chance)

mean_hit_qty(10, 1/6)
"""