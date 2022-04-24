import pandas as pd


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

    @staticmethod
    def find_model_id(model_name):
        datasheets = pd.read_csv('data/datasheets_models_clean.csv', sep='|')
        return datasheets[(datasheets['name'] == model_name)]['datasheet_id'].iloc[0]

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
