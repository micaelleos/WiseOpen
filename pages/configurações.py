
import streamlit as st
from streamlit_google_auth import Authenticate
import plotly.express as px
import time

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='cliente_auth',
    cookie_key='this_is_secret',
    redirect_uri='http://localhost:8501',
)


# Check if the user is already authenticated
authenticator.check_authentification()

df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp",height=100)
fig.update_layout(
    margin=dict(l=20, r=50, t=0, b=0),
    width=200,
)
fig.update_yaxes(visible=False)

alert_success = False

if st.button('Voltar'):
    st.switch_page('pages/inicio.py')

tab1, tab2, tab3 = st.tabs(["Conta", "Pagamentos", "Histórico"])

with tab1:
    with st.container(border=True):
        st.subheader("Configurações de Conta")
        cols = st.columns([0.2,0.8])
        with cols[0]:
            image_url=st.session_state['user_info'].get('picture')
            st.markdown(f'''<div style="margin: 20px 20px 20px 20px; width: 100px; height: 100px; overflow: hidden; border-radius: 80%; display: flex;justify-content: center;align-items: center;">
            <img style="transform: scale(1.05); max-width: 100%; max-height: 100%;" src="{image_url}" alt="Imagem com cropp redondo">
            </div>''',
            unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"<p style='color: black; font-weight: bold; font-size: 16px; margin: 15px 0px 0px 0px'>Nome:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: black; font-size: 16px; margin: 0px 0px 0px 0px'>{st.session_state['user_info'].get('name')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: black; font-weight: bold; font-size: 16px; margin: 0px 0px 0px 0px'>Email:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: black; font-size: 16px; margin: 0px 0px 0px 0px'>{st.session_state['user_info'].get('email')}</p>", unsafe_allow_html=True)

        col1,col2,col3 = st.columns([0.4,0.05,0.4])     
        with col1:
            st.markdown("""<div style = "display: flex; margin: 20px 20px 0px 20px">
                            <div>
                            <p style='color: black; font-weight: bold; font-size: 16px; margin: 0px 0px 0px 0px'>Créditos Restantes:</p>
                            </div>
                            <div>
                                <div style = "display: flex; margin: -20px 20px 20px 20px">
                                        <div>
                                            <p style='color: black; font-size: 24px; margin: 12px 0px 0px 0px'>50</p>
                                        </div>
                                        <div style="margin: 0px 0px 0px 0px; width: 50px; height: 50px; overflow: hidden; border-radius: 80%; display: flex;justify-content: left;align-items: center;">
                                            <img style="transform: scale(4.5); max-width: 100%; max-height: 100%;" src="https://i.pinimg.com/originals/46/94/fd/4694fdf5de28b3084e511d886e208dc4.gif" alt="Imagem com cropp redondo">
                                        </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            st.plotly_chart(fig,use_container_width=True,)

        with col3:                       
            modelo = st.radio("Modelo utilizado no chat",["**Gemini**","**OpenAi**"],captions=["Sem custo", "Com cobrança de Tokens"])
            colx = st.columns(2)
            with colx[0]:
                if st.button('Salvar', use_container_width=True):
                    alert_success = True
                    
            with colx[1]:
                if st.button('Cancelar', use_container_width=True):
                    pass

    if alert_success:
        a = st.success("Configuração salva com sucesso")
        time.sleep(2)
        a.empty()
        alert_success = False

with tab2:
    with st.container(border=True):
        st.subheader("Configurações de Pagamento")
        card_number = st.text_input("Número do Cartão", placeholder="XXX XXX XXX XXX")
        expiration_date = st.text_input("Data de Expiração", placeholder="XX/XX")
        user_name = st.text_input("Nome do Titular", placeholder="João da Silva")
        security = st.text_input("Código de Segurança", placeholder="XXX")

        colx2 = st.columns(3)
        with colx2[2]:
            if st.button('Salvar dados do cartão'):
                alert_success = True
    if alert_success:
        b = st.success("Cartão salvo com sucesso")
        time.sleep(2)
        b.empty()
        alert_success = False

with tab3:
    with st.container(border=True):
        st.subheader("Histórico de Pagamento")
        st.dataframe(df)  


st.markdown("""
<style>
    .st-emotion-cache-1dp5vir {
        position: absolute;
        top: 0px;
        right: 0px;
        left: 0px;
        height: 0.125rem;
        background-image: linear-gradient(90deg, rgb(50, 10, 255), rgb(255, 128, 197));
        z-index: 999990;
    }
    .st-emotion-cache-1y4p8pa {
    width: 100%;
    padding: 4rem 1rem 10rem;
    max-width: 46rem;
    }           
</style>

""",unsafe_allow_html=True)