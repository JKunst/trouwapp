import streamlit as st
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

name, authentication_status, username = authenticator.login('main', fields={
    'Form name': 'Gebruik de login code van de uitnodiging'})

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
worksheet2 = sh.get_worksheet(1)


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

    if username == 'bruiloftsgast':
        st.write(f'Welkom *{name}*')
        st.write('Onderstaande kadolijst is gedeeld met alle gasten, je kan zien of een item al is afgestreept. Geef aan als je '
                 'iets gekocht hebt')
        list_of_lists = worksheet2.get_all_values()
        presenteer_data = pd.DataFrame(list_of_lists,columns=['Kado','Beschikbaar'])
        st.button('Ververs')
        for index, row in presenteer_data.iterrows():
             if index == 0: continue
             st.markdown("""---""")
             st.write(row['Kado'] + ".        "+ row['Beschikbaar'])#
             if row['Beschikbaar']=='':
                 if st.button(label='Streep dit af', key=index):
                     st.text('Je geeft aan dit te kopen')
                     worksheet2.update_cell(index+1, 2, 'Dit item is afgestreept!')
                     st.rerun()
             if row['Beschikbaar'] != '':
                 if st.button(label='Maak dit kado weer beschikbaar', key=index*100):
                    st.text('Het kado is weer beschikbaar')
                    worksheet2.update_cell(index + 1, 2, '')
                    st.rerun()
        st.markdown("""---""")
        st.write("Sharon, Jasper en Frederik kunnen een donatie aan de Stichting Steun Emma kinderziekenhuis ook erg waarderen. Doneren kan via https://www.steunemma.nl .")
        st.markdown("""---""")
        st.write(
            "Sharon, Jasper en Frederik kunnen een donatie aan hun huwelijksreis ook waarderen.")
        st.markdown("""---""")
        st.write("Niks kunnen vinden? Kom later terug voor meer kado's")
    st.markdown('''---''')
    st.page_link("pages/Dresscode.py", label="Dresscode", icon=":material/arrow_forward:")
    st.page_link("Welkom.py", label="Welkom", icon=":material/arrow_forward:")
    st.page_link("pages/Routebeschrijving.py", label="Routebeschrijving", icon=":material/arrow_forward:")
                #st.table(presenteer_data.iloc[1:])

    authenticator.logout('Logout', 'main')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.session_state.sidebar_state = 'collapsed'

    st.warning('Please enter your username and password')