import sqlite3

import pandas as pd


def connect_to_database(f):
    def wrap(*args):
        with sqlite3.connect('test.sqlite') as con:
            cur = con.cursor()
            connected = f(cur, *args)
            return connected

    return wrap


@connect_to_database
def find_model_id(cursor, model_name):
    request = cursor.execute(
        f'select datasheet_id from datasheets_models where name=:name',
        {'name': model_name}
    )
    return int(request.fetchone()[0])


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


id = find_model_id('Necron Warrior')
wg_list = get_wargear_list(id)

print(wg_list)
