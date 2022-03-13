import re

from model_stats import Model
import random


class Shooting:
    def __init__(self, attacker, defender):
        self.defender = defender
        self.attacker = attacker

    @staticmethod
    def roll():
        return random.randint(1, 6)

    @staticmethod
    def dx_roll(x):
        return random.randint(1, x)

    def hit(self):
        roll = self.roll()
        return roll >= self.attacker.ws

    def wound(self):
        roll = self.roll()
        if self.attacker.weapon_S >= self.defender.t * 2:
            required_roll = 2
        elif self.attacker.weapon_S > self.defender.t:
            required_roll = 3
        elif self.attacker.weapon_S == self.defender.t:
            required_roll = 4
        elif self.attacker.weapon_S <= self.defender.t / 2:
            required_roll = 6
        else:  # self.weapon_s < defender_t
            required_roll = 5
        return roll >= required_roll

    def attack(self):
        if self.hit():
            if self.wound():
                return self.defender.sv > \
                       self.roll() + self.attacker.weapon_AP
        return False

    def damage_chance(self, n=100000):
        summ = 0
        for i in range(0, n):
            summ += self.attack()
        return summ / n

    def mean_roll_result(self, string, n=100000):
        summ = 0
        for i in range(0, n):
            summ += self.find_roll_result(string)
        return summ / n

    def find_roll_result(self, string):
        template = ' D.'
        template2 = '[0-9]*D.'
        template3 = ' [0-9]'
        if re.search(template, string):
            x = int(string[-1])
            roll_result = self.dx_roll(x)
        elif re.search(template2, string):
            search = re.search(template2, string)
            multiplier = int(search[0][0])
            x = int(search[0][-1])
            roll_result = self.dx_roll(x) * multiplier
        elif re.search(template3, string):
            roll_result = int(string[-1])
        else:
            raise ValueError('Incorrect roll data')
        return roll_result

    def mean_wound_qty(self):
        string = self.attacker.weapon_type
        p = self.damage_chance() * self.mean_roll_result(string=string)
        if 'Rapid Fire' in string:
            return 2 * p
        return p


if __name__ == "__main__":
    marine = Model('Intercessor', 'Bolt pistol')
    necron = Model('Necron Warrior', 'Gauss flayer')
   # necron = Model('Skorpekh Lord', 'Enmitic annihilator')
   # necron = Model('Illuminor Szeras', 'Eldritch Lance (shooting)')
    #necron = Model('Lord', 'Staff of light (shooting)')

    shoot = Shooting(necron, marine)
    print(shoot.mean_wound_qty())
