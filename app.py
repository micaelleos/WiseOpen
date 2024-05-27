import streamlit as st
from streamlit_google_auth import Authenticate

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='cliente_auth',
    cookie_key='this_is_secret',
    redirect_uri='http://localhost:8501',
)

# Check if the user is already authenticated
authenticator.check_authentification()


# Display the login button if the user is not authenticated
if not st.session_state.get('connected', True):
    st.markdown('Bem vindo ao aplicativo WiseOpen. Para acessar faça login com sua conta google:')
    authenticator.login(justify_content='flex-start')
    #authorization_url = authenticator.get_authorization_url()
    #st.link_button('Login', authorization_url)
    #st.markdown(f'<a href="{authorization_url}" target="_self"><button style="background-color: #4CAF50; /* Green */ border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">Fazer Login</button></a>', unsafe_allow_html=True)

else:
    st.switch_page("pages/inicio.py")