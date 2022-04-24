import pandas as pd
import sqlite3


def connect_to_database(f):
    def wrap(self, *args):
        with sqlite3.connect('test.db') as con:
            cur = con.cursor()
            connected = f(self, cur, *args)
            return connected

    return wrap


class Model:
    def __init__(self, name, weapon):
        model_id = self.find_model_id(name)
        datasheets_m = pd.read_csv('data/datasheets_models_clean.csv', sep='|')
        row = datasheets_m[(datasheets_m['datasheet_id'] == model_id)]
        row = row.iloc[0]
        self.name = row['name']
        self.m = int(row['M'][:-2])
        self.ws = int(row['WS'][0])
        self.bs = int(row['BS'][0])
        self.s = row['S']
        self.t = int(row['T'])
        self.w = row['W']
        self.a = row['A']
        self.ld = row['Ld']
        self.sv = int(row['Sv'][0])
        self.weapon_name = weapon
        weapon_row = self.get_wargear_list(model_id)
        for wg in weapon_row:
            wg = wg.iloc[0]
            if wg['name'] == self.weapon_name:
                self.weapon_type = wg['type']
                # self.weapon_type = wg['type'][:-1]
                # self.weapon_shots = int(wg['type'][-1])
                self.weapon_S = int(wg['S'])
                self.weapon_AP = int(wg['AP'])
                self.weapon_D = wg['D']
                # self.weapon_D = int(wg['D'])

    @connect_to_database
    def find_model_id(self, cursor, model_name):
        i = cursor.execute(
            f'select datasheet_id from datasheets_models where name=:name',
            {'name': model_name})
        return int(i.fetchone()[0])

    @staticmethod
    def get_wargear_list(model_id):
        datasheets_warg = pd.read_csv('data/datasheets_wargear_clean.csv',
                                      sep='|')
        wargear_list = pd.read_csv('data/wargear_list_clean.csv', sep='|')
        wargear = []
        row = datasheets_warg[(datasheets_warg['datasheet_id'] == model_id)]
        wg_ids = row['wargear_id'].values
        for i in wg_ids:
            wargear.append(wargear_list[(wargear_list['wargear_id'] == i)])
        return wargear
