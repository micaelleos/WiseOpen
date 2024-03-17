import streamlit as st

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
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    '''if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()'''
    header()
    st.sidebar.page_link("app.py", label="Início")
    st.sidebar.page_link("pages/main.py", label="Wize")
    st.sidebar.page_link("pages/upload_norma.py", label="Repositório de normas")


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    #if "role" not in st.session_state or st.session_state.role is None:
    #    st.switch_page("app.py")
    menu()