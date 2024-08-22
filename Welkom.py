import streamlit as st
import pandas as pd
import numpy as np
#
from streamlit_authenticator.utilities.hasher import Hasher
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
credentials = {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "universe_domain": st.secrets["universe_domain"],
}
gc = gs.service_account_from_dict(credentials)
#lokaal
#gc = gs.service_account(filename='cred.json')


sh = gc.open('Feedback gasten')
worksheet = sh.sheet1


def send(A1, A2, A3, A4, A5, A6, A7):
    data_gast = [A1, A2, A3, A4, A5, A6, A7]
    worksheet.append_row(data_gast, table_range="A1:F1")
    data_gast_2 = pd.DataFrame(data_gast, index=['Naam','Plus','Reactie', 'Dieetwensen', 'MTB', 'Opmerkingen','Nummer'], columns=['Je reactie'])
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
        st.markdown('''---''')
        st.page_link("pages/Dresscode.py", label="Dresscode", icon=":material/arrow_forward:")
        st.page_link("pages/Kadolijst.py", label="Kadolijst", icon=":material/arrow_forward:")
        st.page_link("pages/Routebeschrijving.py", label="Routebeschrijving", icon=":material/arrow_forward:")

    if username == 'bruiloftsgast':
        st.write(f'Welkom *{name}*')
        st.image('graphics/img1.jpg')
        st.subheader('De voorbereidingen zijn in volle gang')
        st.text('Voer hieronder alsjeblieft wat informatie in')
        gast_naam = st.text_input('Je naam')
        gast_plus_een = st.text_input('Je +1', value='Ik kom alleen')
        rsvp = st.selectbox('Je reactie:',['Ik ben er bij.','Ik ben er niet bij.','Ik ben er deels bij, bel mij om te overleggen.'])
        dieet = st.text_input('Eventuele dieetwensen')
        mtb = st.selectbox('Mountainbiken?',['Ik laat het nog weten','Nee, maar veel plezier.', 'Ja, ik breng mijn eigen fiets mee','Ja, huur een fiets voor mij'])
        opmerkingen = st.text_input('Aanvullend')
        telefoonnummer = st.text_input('Indien nodig je telefoonnummer')

        if st.button('Verzenden', key=None, help=None):
            send(gast_naam, gast_plus_een, rsvp, dieet, mtb, opmerkingen, telefoonnummer)
        st.text(
            ' \n'
        )
        st.markdown('''---''')
        st.page_link("pages/Dresscode.py", label="Dresscode", icon=":material/arrow_forward:")
        st.page_link("pages/Kadolijst.py", label="Kadolijst", icon=":material/arrow_forward:")
        st.page_link("pages/Routebeschrijving.py", label="Routebeschrijving", icon=":material/arrow_forward:")
        st.page_link("pages/FAQ.py", label="FAQ", icon=":material/arrow_forward:")

        ########### Fotograaf
    if username == 'fotograaf':

        st.write(f'Welkom *{name}*')
        st.image('graphics/img1.jpg')
        st.subheader('Hieronder vind je de informatie over onze gasten')
        #ouders
        st.subheader('Ouders Sharon, Rienco + Marleen')
        foto2 = st.checkbox("Gevangen", key=2)
        st.image('graphics/rienco.jpg')
        st.subheader('Ouders Jasper, Piet + Irene')
        foto1 = st.checkbox("Gevangen", key=1)
        st.image('graphics/piet.jpg')

        #Zusjes
        st.subheader('Zusje Sharon, Judith + Ivo')
        foto5 = st.checkbox("Gevangen", key=5)
        st.image('graphics/judith.jpg')

        st.subheader('Zusje Sharon, Rachel + Stefan')
        foto6 = st.checkbox("Gevangen", key=6)
        st.image('graphics/rachel.jpg')

        st.subheader('Zus Jasper, Willemijn + Jurgen + (Pepijn en Yentl)')
        foto3 = st.checkbox("Gevangen", key=3)
        st.image('graphics/willemijn.jpg')
        st.image('graphics/willemijngezin.jpg')

        st.subheader('Zusje Jasper, Elsemieke + Bram')
        foto4 = st.checkbox("Gevangen", key=4)
        st.image('graphics/elsemieke.jpg')

        #oma's
        st.subheader('Oma Verschelling + (Jack en Bea)')
        foto7 = st.checkbox("Gevangen", key=7)
        #st.image('graphics/oma martijn teresa.jpg')

        st.subheader('Opa en oma Dieleman')
        foto8 = st.checkbox("Gevangen", key=8)
        #st.image('graphics/omi.jpg')

        st.subheader('Oma Kunst (+Martijn + Teresa)')
        foto9 = st.checkbox("Gevangen", key=9)
        st.image('graphics/oma martijn teresa.jpg')

        st.subheader('Oma Janssens (+ Mathijs)')
        foto10 = st.checkbox("Gevangen", key=10)
        st.image('graphics/omi.jpg')

        #Vrienden
        st.subheader('Wouter en Marthe')
        foto101 = st.checkbox("Gevangen", key=101)
        st.image('graphics/wouter.jpg')

        st.subheader('Jim en Bente')
        foto102 = st.checkbox("Gevangen", key=102)
        st.image('graphics/jim.jpg')






        st.markdown('''---''')
        st.page_link("pages/Dresscode.py", label="Dresscode", icon=":material/arrow_forward:")
        st.page_link("pages/Kadolijst.py", label="Kadolijst", icon=":material/arrow_forward:")
        st.page_link("pages/Routebeschrijving.py", label="Routebeschrijving", icon=":material/arrow_forward:")
    authenticator.logout('Logout', 'main')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.session_state.sidebar_state = 'collapsed'

    st.warning('Please enter your username and password')



