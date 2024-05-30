import streamlit as st
from streamlit_google_auth import Authenticate

st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)



pop_over_container = f"""
    <div style="display: flex; width: 80%; max-width: 1200px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
        <div style="flex: 3; padding: 20px; display: flex; align-items: center;">
            <div style="display: flex; align-items: center;">
                <img src="{st.session_state['user_info'].get('picture')}" alt="Foto do Usuário" style="border-radius: 50%; margin-right: 20px;">
                <div style="display: flex; flex-direction: column;">
                    <span style="margin-bottom: 5px;">Nome do Usuário</span>
                    <span>email@exemplo.com</span>
                </div>
            </div>
        </div>
        <div style="flex: 1; padding: 20px; display: flex; justify-content: flex-end; align-items: center;">
            <button style="padding: 10px 20px; background-color: #d9534f; color: #fff; border: none; border-radius: 4px; cursor: pointer;" 
                onmouseover="this.style.backgroundColor='#c9302c'" 
                onmouseout="this.style.backgroundColor='#d9534f'">Logoff</button>
        </div>
    </div>
"""

authenticator = st.session_state['authenticator']

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
    st.sidebar.page_link("pages/chat.py", label="Your profile")
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

def user_logged():
    with st.sidebar:
        st.container(height=80, border=False)
        with st.container(border=True):
            cols = st.columns([0.2, 0.6, 0.4])
            
            with cols[0]:
                image_url=st.session_state['user_info'].get('picture')
                st.markdown(f'''<div style="margin: 0px 20px 0px 0px; width: 40px; height: 40px; overflow: hidden; border-radius: 100%; display: flex;justify-content: center;align-items: center;">
                <img style="max-width: 100%;max-height: 100%;" src="{image_url}" alt="Imagem com cropp redondo">
                </div>''',
                unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown(f"<p style='color: black; font-size: 14px; margin: 10px 20px 0px 0px'>{st.session_state['user_info'].get('name')}</p>", unsafe_allow_html=True)
                #st.markdown(f"<p style='color: black; font-size: 12px; margin: 0px 20px 0px 0px'>{st.session_state['user_info'].get('email')}</p>", unsafe_allow_html=True)

            with cols[2]:
                with st.popover(":gear:",use_container_width=True):
                    #st.markdown(pop_over_container,unsafe_allow_html=True)
                    if st.button("Configurações", use_container_width=True):
                        st.switch_page("pages/configurações.py")
                    if st.button("Logout",use_container_width=True):
                        authenticator.logout()

def menu():
    # navigation menu
    #header()
    st.sidebar.page_link("pages/inicio.py", label="Início")
    st.sidebar.page_link("pages/chat.py", label="Wize")
    st.sidebar.page_link("pages/upload_norma.py", label="Repositório de normas")
    with st.sidebar:
        st.write('-----------')
    user_logged()

    

def menu_with_redirect():
    # Display the login button if the user is not authenticated
    if not st.session_state.get('connected', False):
        st.switch_page("app.py")
    # Display the user information and logout button if the user is authenticated
    else:
        menu()
