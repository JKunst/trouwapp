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
        st.write("Als dresscode zien we u graag een beetje stijlvol en chique. \n"
                "Lekker feestelijk, dit heet schijnbaar tenue de ville")
    if username == 'bruiloftsgast':
        st.subheader('Tot hoe laat duurt het  feest?')
        st.write("Het feest eindigt om 00:00.")
        st.subheader('Mag er gedurende de dag in de fontein gezwommen worden?')
        st.write("Nee, het zwemmen in de fontein is alleen voor eendjes.")
        st.subheader("Welk gereedschap moet ik meenemen om het dak eraf te halen?")
        st.write("In principe zijn alle randvoorwaarden voor een feestje aanwezig. Een eigen schroevendraaier of 10/13 kun je thuis laten.")
        st.subheader("Mag ik op de bar dansen.")
        st.write("It depends.")
    st.markdown('''---''')
    st.page_link("pages/Kadolijst.py", label="Kadolijst", icon=":material/arrow_forward:")
    st.page_link("Welkom.py", label="Welkom", icon=":material/arrow_forward:")
    st.page_link("pages/Routebeschrijving.py", label="Routebeschrijving", icon=":material/arrow_forward:")
    st.page_link("pages/Dresscode.py", label="Dresscode", icon=":material/arrow_forward:")

    authenticator.logout('Logout', 'main')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.session_state.sidebar_state = 'collapsed'

    st.warning('Please enter your username and password')
