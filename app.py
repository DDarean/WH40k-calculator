import streamlit as st

from calculator import Shooting
from db import find_model_id, get_wargear_list
from model_stats import Model
import plotly.express as px
import pandas as pd

attacker_txt = st.text_input('Attacker', value='Necron Warrior')
if attacker_txt:
    id = find_model_id(attacker_txt)
    wg_list = get_wargear_list(id)
    columns = ['name', 'Range', 'type', 'S', 'AP', 'D']
    st.write(wg_list[columns])
    weapon = st.radio(
        "Select weapon",
        wg_list['name'].values)
n_units = int(st.text_input('Number of units', value=10))
attacker = Model(attacker_txt, weapon)

defender_txt = st.text_input('Defender', value='Intercessor')
if defender_txt and attacker_txt:
    defender = Model(defender_txt)
    calc = Shooting(attacker, defender)
    h, w, u = calc.count_statistics_total(n_units=n_units)
    fig = px.bar(pd.DataFrame(h, index=["hits"]).T, y='hits')
    st.plotly_chart(fig)
    fig = px.bar(pd.DataFrame(w, index=["wounds"]).T, y='wounds')
    st.plotly_chart(fig)
    fig = px.bar(pd.DataFrame(u, index=["unsaved"]).T, y='unsaved')
    st.plotly_chart(fig)
