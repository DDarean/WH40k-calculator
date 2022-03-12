from model_stats import Model
import random


class Shooting:
    def __init__(self, attacker, defender):
        self.defender = defender
        self.attacker = attacker

    @staticmethod
    def roll():
        return random.randint(1, 6)

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

    def mean_wound_qty(self, n=1):
        p = self.damage_chance()
        #low = round(n * p - (1 - p), 2)
        #high = round(n * p + p, 2)
        return n * p#(low + high) / 2

    def mean_damage(self, n=1):
        return self.mean_wound_qty(n) * self.attacker.weapon_shots


if __name__ == "__main__":
    marine = Model('Intercessor', 'Bolt pistol')
    necron = Model('Necron Warrior', 'Gauss flayer')

    shoot = Shooting(necron, marine)
    print(shoot.mean_damage())
