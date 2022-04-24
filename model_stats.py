import sqlite3

import pandas as pd


def connect_to_database(f):
    def wrap(*args):
        with sqlite3.connect('test.db') as con:
            cur = con.cursor()
            connected = f(cur, *args)
            return connected

    return wrap


class Model:
    def __init__(self, name, weapon=None):
        model_id = self.find_model_id(name)
        row = self.get_model_stats(model_id)
        row = row[(row['name'] == name)]
        self.name = row['name']
        self.m = int(row['M'][0][:-2])
        self.ws = int(row['WS'][0][0])
        self.bs = int(row['BS'][0][0])
        self.s = row['S'][0]
        self.t = int(row['T'][0])
        self.w = row['W'][0]
        self.a = row['A'][0]
        self.ld = row['Ld'][0]
        self.sv = int(row['Sv'][0][0])

        if weapon:
            self.weapon_name = weapon
            weapon_row = self.get_wargear_list(model_id)
            weapon_row = weapon_row[weapon_row['name'] == self.weapon_name]
            self.weapon_type = weapon_row['type'].values[0]
            self.weapon_S = int(weapon_row['S'])
            self.weapon_AP = int(weapon_row['AP'])
            self.weapon_D = weapon_row['D']

    @staticmethod
    @connect_to_database
    def find_model_id(cursor, model_name):
        request = cursor.execute(
            f'select datasheet_id from datasheets_models where name=:name',
            {'name': model_name}
        )
        return int(request.fetchone()[0])

    @staticmethod
    @connect_to_database
    def get_model_stats(cursor, model_id):
        model_stats = cursor.execute(
            f'select * from datasheets_models where datasheet_id=:id',
            {'id': model_id}
        )
        names = list(map(lambda x: x[0], cursor.description))
        df_stats = pd.DataFrame(model_stats.fetchall(), columns=names)
        return df_stats

    @staticmethod
    @connect_to_database
    def get_wargear_list(cursor, model_id):
        wargear = []
        wargear_ids = cursor.execute(
            f'select wargear_id from datasheets_wargear where datasheet_id=:id',
            {'id': model_id}
        )
        for id in wargear_ids.fetchall():
            wg_stats = cursor.execute(
                f'select * from wargear_list where wargear_id=:wg_id',
                {'wg_id': id[0]}
            )
            wargear.append(wg_stats.fetchall())
        wargear = [x for lst in wargear for x in lst]
        names = list(map(lambda x: x[0], cursor.description))
        df_wargear = pd.DataFrame(wargear, columns=names)
        return df_wargear

