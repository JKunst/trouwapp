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
        st.text("Nog bepalen")
    if username == 'bruiloftsgast':
        st.write(f'Welkom *{name}*')
        st.subheader('Openbaar vervoer')
        st.write("Met het ov reist u het makkelijkst naar station Hilversum en pakt u een ov-fiets.\n"
                "De fietsenstalling is tot half 2 's nachts geopend. Check voor u vertrekt uw reis in de ns app.")
        st.markdown('''---''')
        st.subheader("Auto")
        st.write("Met de auto kunt u parkeren op het terrein van het kasteel. \n"
                "Rijdt door het hek rechtsom tot u op de parkeerplaats komt.")
        st.markdown('''---''')
        st.subheader("Adres")
        st.write("[Hilversumsestraatweg 14, 3744 KC Baarn](https://www.google.com/maps/place//data=!4m2!3m1!1s0x47c66a89b7fcca8b:0x9c6894d987984a2f?sa=X&ved=1t:8290&ictx=111)")


        st.markdown('''---''')
        st.page_link("pages/Dresscode.py", label="Dresscode", icon=":material/arrow_forward:")
        st.page_link("Welkom.py", label="Welkom", icon=":material/arrow_forward:")
        st.page_link("pages/Kadolijst.py", label="Kadolijst", icon=":material/arrow_forward:")

    authenticator.logout('Logout', 'main')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.session_state.sidebar_state = 'collapsed'

    st.warning('Please enter your username and password')