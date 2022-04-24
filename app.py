import matplotlib.pyplot as plt
import streamlit as st

from calculator import Shooting
from db import find_model_id, get_wargear_list
from model_stats import Model

attacker_txt = st.text_input('Attacker', value='Necron Warrior')
if attacker_txt:
    id = find_model_id(attacker_txt)
    wg_list = get_wargear_list(id)
    columns = ['name', 'Range', 'type', 'S', 'AP', 'D']
    st.write(wg_list[columns])
    weapon = st.radio(
        "Select weapon",
        wg_list['name'].values)
n_units = int(st.text_input('Number of units', value=1))
attacker = Model(attacker_txt, weapon)

defender_txt = st.text_input('Defender', value='Intercessor')
if defender_txt and attacker_txt:
    defender = Model(defender_txt)
    calc = Shooting(attacker, defender)
    h, w, u = calc.count_statistics_total(n_units=n_units)

    fig, ax = plt.subplots(1, 3, figsize=(10, 5))
    ax[0].bar(h.keys(), h.values())
    ax[0].set_title('Hits')
    ax[1].bar(w.keys(), w.values())
    ax[1].set_title('Wounds')
    ax[2].bar(u.keys(), u.values())
    ax[2].set_title('Unsaved wounds')
    st.pyplot(fig)
