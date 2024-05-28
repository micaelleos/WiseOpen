import streamlit as st
from streamlit_google_auth import Authenticate

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='cliente_auth',
    cookie_key='this_is_secret',
    redirect_uri='http://localhost:8501',
)


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
    header()
    st.sidebar.page_link("pages/inicio.py", label="Início")
    st.sidebar.page_link("pages/main.py", label="Wize")
    st.sidebar.page_link("pages/upload_norma.py", label="Repositório de normas")

    with st.sidebar:
        #st.markdown('<div style="margin: -500px 0px -25px 0px;></div>', unsafe_allow_html=True)
        st.container(height=80,border=False)
        with st.container(border=False):
            image_url=st.session_state['user_info'].get('picture')
            col1,col2 =st.columns([1, 2])
            with col1:
                st.markdown(f'''<div style="margin: 0px 20px 0px 0px; width: 70px; height: 70px; overflow: hidden; border-radius: 100%; display: flex;justify-content: center;align-items: center;">
                            <img style="max-width: 100%;max-height: 100%;" src="{image_url}" alt="Imagem com cropp redondo">
                            </div>''',
                unsafe_allow_html=True)
            #st.image(st.session_state['user_info'].get('picture'))
            with col2:
                #st.write(f"Hello, {st.session_state['user_info'].get('name')} {st.session_state['user_info'].get('email')}")
                st.markdown(f"<p style='color: black; font-size: 14px; margin: 0px 20px 0px 0px'>{st.session_state['user_info'].get('name')}</p>", unsafe_allow_html=True)
                if st.button('configurações',use_container_width=True):
                    st.switch_page("pages/configurações.py")
    

def menu_with_redirect():
    # Display the login button if the user is not authenticated
    if not st.session_state.get('connected', False):
        st.switch_page("app.py")
    # Display the user information and logout button if the user is authenticated
    else:
        menu()
