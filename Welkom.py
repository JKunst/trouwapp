import streamlit as st
import pandas as pd
import numpy as np
#
st.set_page_config(initial_sidebar_state="collapsed")
st.session_state.sidebar_state = 'collapsed'
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

#Initiating link to worksheet
import gspread as gs
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
gc = gs.service_account(filename='../cred.json')
sh = gc.open('Feedback gasten')
worksheet = sh.sheet1


def send(A1, A2, A3, A4, A5, A6):
    data_gast = [A1, A2, A3, A4, A5, A6]
    worksheet.append_row(data_gast, table_range="A1:F1")
    data_gast_2 = pd.DataFrame(data_gast, index=['Naam','Plus','Reactie', 'Dieetwensen','Opmerkingen','Nummer'], columns=['Je reactie'])
    return st.text('Je reactie is verzonden'), st.table(data_gast_2), st.text('Als er iets niet klopt doe je het gewoon opnieuw!')


import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)


name, authentication_status, username = authenticator.login('main',fields = {'Form name': 'Gebruik de login code van de uitnodiging'})

if authentication_status:
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: initial
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.success("Klik hierboven voor meer info.")
    # page content
    st.title('Sharon en Jasper gaan trouwen!')
    if username == 'ceremoniemeester':

        st.write(f'Welkom *{name}*')
        st.image('graphics/img1.jpg')
        st.subheader('De voorbereidingen zijn in volle gang')
        st.text('Tot nu toe aangemeld:')
        st.button('Ververs')
        list_of_lists = worksheet.get_all_values()
        presenteer_data = pd.DataFrame(list_of_lists,columns=['Naam','Plus','Reactie', 'Dieetwensen','Opmerkingen','Nummer'])
        st.table(presenteer_data.iloc[1:])
    if username == 'daggast':
        st.write(f'Welkom *{name}*')
        st.image('graphics/img1.jpg')
        st.subheader('De voorbereidingen zijn in volle gang')
        st.text('Voer hieronder alsjeblieft wat informatie in')
        gast_naam = st.text_input('Je naam')
        gast_plus_een = st.text_input('Je plus 1 of betere helft')
        rsvp = st.selectbox('Je reactie:',['Ik ben er bij.','Ik ben er niet bij.','Ik ben er deels bij., bel mij om te overleggen.'])
        dieet = st.text_input('Eventuele dieetwensen')
        opmerkingen = st.text_input('Aanvullend')
        telefoonnummer = st.text_input('Indien nodig je telefoonnummer')

        if st.button('Verzenden', key=None, help=None):
            send(gast_naam, gast_plus_een, rsvp, dieet, opmerkingen, telefoonnummer)


    authenticator.logout('Logout', 'main')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.session_state.sidebar_state = 'collapsed'

    st.warning('Please enter your username and password')



