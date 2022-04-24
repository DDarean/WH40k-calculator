import random
import re
from collections import Counter


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

    def save(self):
        return self.defender.sv - self.attacker.weapon_AP > self.roll()

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

    def count_statistics_one_round(self, n_units=1):
        string = self.attacker.weapon_type
        hits = []
        wounds = []
        unsaved = []

        for _ in range(0, n_units):
            num_of_attacks = self.find_roll_result(string)
            for _ in range(0, num_of_attacks):
                hits.append(self.hit())
        hits_total = sum(hits)

        for i in range(0, hits_total):
            wounds.append(self.wound())
        wounds_total = sum(wounds)

        for i in range(0, wounds_total):
            unsaved.append(self.save())
        unsaved_total = sum(unsaved)

        return hits_total, wounds_total, unsaved_total

    def count_statistics_total(self, n_simulations=10000, n_units=1):
        h = []
        w = []
        u = []
        for i in range(0, n_simulations):
            hits, wounds, unsaved = self.count_statistics_one_round(n_units=n_units)
            h.append(hits)
            w.append(wounds)
            u.append(unsaved)
        counts_h = Counter(h)
        counts_w = Counter(w)
        counts_u = Counter(u)
        return counts_h, counts_w, counts_u
