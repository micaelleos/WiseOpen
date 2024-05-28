
import streamlit as st
from streamlit_google_auth import Authenticate

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='cliente_auth',
    cookie_key='this_is_secret',
    redirect_uri='http://localhost:8501',
)

with st.form('addition'):
    a = st.number_input('a')
    b = st.number_input('b')
    submit = st.form_submit_button('add')

if submit:
    st.title(f'oi')

if st.button('Log out'):
    authenticator.logout()

if st.button('Voltar'):
    authenticator.logout()