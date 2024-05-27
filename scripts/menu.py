import streamlit as st
from streamlit_google_auth import Authenticate

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='cliente_auth',
    cookie_key='this_is_secret',
    redirect_uri='http://localhost:8501',
)

hide_footer_style = '''
<style>
.reportview-container .main footer {visibility: hidden;}
'''
st.markdown(hide_footer_style, unsafe_allow_html=True)

hide_menu_style = '''
<style>
#MainMenu {visibility: hidden;}
</style>
'''

st.markdown(hide_menu_style, unsafe_allow_html=True)

def header():
    with st.sidebar:
        with st.columns([1, 2, 1])[1]:
            st.image('src\img\owl Open.png', use_column_width="always")
        st.markdown("<p style='font-weight: bold; font-size: 36px; text-align: center; color: #4a7e94; margin: -20px 0px -25px 0px'>Wize Normas</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: black; margin: -20px 0px -20px 0px'>Open Finance Brasil</h1>", unsafe_allow_html=True)
        st.write("Entendendo de forma fácil as normativas.")
     

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="Switch accounts")
    st.sidebar.page_link("pages/main.py", label="Your profile")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link(
            "pages/upload_norma.py",
            label="Manage admin access",
            disabled=st.session_state.role != "super-admin",
        )


def unauthenticated_menu():
    # Check if the user is already authenticated
    authenticator.check_authentification()
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    # navigation menu
    '''if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()'''
    header()
    st.sidebar.page_link("pages/inicio.py", label="Início")
    st.sidebar.page_link("pages/main.py", label="Wize")
    st.sidebar.page_link("pages/upload_norma.py", label="Repositório de normas")
    with st.sidebar:
        st.image(st.session_state['user_info'].get('picture'))
        st.write(f"Hello, {st.session_state['user_info'].get('name')}")
        st.write(f"Your email is {st.session_state['user_info'].get('email')}")
        
        if st.button('Log out'):
            authenticator.logout()

    

def menu_with_redirect():
    # Display the login button if the user is not authenticated
    if not st.session_state.get('connected', False):
        st.switch_page("app.py")
    # Display the user information and logout button if the user is authenticated
    else:
        menu()
