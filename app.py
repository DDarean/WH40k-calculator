import streamlit as st

from calculator import Shooting
from db import find_model_id, get_wargear_list
from model_stats import Model
import plotly.express as px
import pandas as pd
st.set_page_config(layout='wide')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 600px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 600px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    attacker_txt = st.text_input('Attacker', value='Necron Warrior')

    if attacker_txt:
        id = find_model_id(attacker_txt)
        wg_list = get_wargear_list(id)
        columns = ['name', 'Range', 'type', 'S', 'AP', 'D']
        st.write(wg_list[columns])
        weapon = st.radio(
            "Select weapon",
            wg_list['name'].values)

    attacker = Model(attacker_txt, weapon)
    rapid_fire_flag = False
    if 'Rapid Fire' in attacker.weapon_type:
        rapid_fire_flag = st.checkbox('Rapid fire (x2 attack)', value=False)

    n_units = int(st.text_input('Number of units', value=10))

    defender_txt = st.text_input('Defender', value='Intercessor')


if defender_txt and attacker_txt:

    defender = Model(defender_txt)
    calc = Shooting(attacker, defender)
    h, w, u = calc.count_statistics_total(n_units=n_units,
                                          rapid_fire_flag=rapid_fire_flag)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(pd.DataFrame(h, index=["hits"]).T, y='hits')
        fig.update_layout(title_text='Hits', title_x=0.5)
        st.plotly_chart(fig)

    with col2:
        fig = px.bar(pd.DataFrame(w, index=["wounds"]).T, y='wounds')
        fig.update_layout(title_text='Wounds', title_x=0.5)
        st.plotly_chart(fig)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.bar(pd.DataFrame(u, index=["unsaved"]).T, y='unsaved')
        fig.update_layout(title_text='Unsaved hits', title_x=0.5)
        st.plotly_chart(fig)

    with col4:
        st.title('Expected values', anchor=None)
        st.write(f'Successful hits: {max(h, key=h.get)}')
        st.write(f'Successful wounds: {max(w, key=w.get)}')
        st.write(f'Unsaved hits: {max(u, key=u.get)}')
