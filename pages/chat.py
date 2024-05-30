import streamlit as st
import time
from scripts.menu import menu_with_redirect, menu
#from scripts.llm_gemini import Gemini_chat
from scripts.llm_openai import OpenAI_chat
import json
from streamlit_google_auth import Authenticate

st.markdown("""
    <style>
    .st-emotion-cache-1y4p8pa {
    width: 100%;
    padding: 3rem 1rem 0rem 3rem;
    max-width: 70rem;
    margin: 0rem 0rem 0rem -10rem
    }
    .st-emotion-cache-w07wwc {
    width: 918px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    height : 60vh;
    }        

    </style>
""", unsafe_allow_html=True)

#st.markdown(f"""<div>{
#        st.expander('Documentos para consulta',expanded=False).write('''
#            The chart above shows some numbers I picked for you.
#            I rolled actual dice for these, so they're *guaranteed* to
#            be random.
#        ''')
#}</div>""",unsafe_allow_html=True)


# Show the navigation menu
menu_with_redirect()

col=st.columns([0.3,0.7])
with st.container():
    with col[0]:
        with st.expander('Documentos para consulta',expanded=False):
            st.write('''
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        ''')

with st.container():
    with col[1]:
        st.title("Wize Normas Open Finance")
        with st.container(height=500, border=False):
            # Streamed response emulator
            def response_generator(response):
                time.sleep(0.05)
                for word in response.split(" "):
                    yield word+ " "
                    time.sleep(0.05)

            with st.spinner(''):
                # Importando motor do wise
                #wise = Gemini_chat()
                wise = OpenAI_chat()

            initial_message = st.chat_message("assistant", avatar='src\img\owl Open.png')
            initial_message.write(response_generator("Olá, como posso ajudá-lo hoje?"))  

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                if message['role'] == "assistant":
                    avatar = 'src\img\owl Open.png'
                    with st.chat_message(message["role"], avatar=avatar):
                        st.markdown(message["content"])
                else:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                

            if prompt := st.chat_input("Faça uma pergunta?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant", avatar='src\img\owl Open.png'):
                    with st.spinner(''):
                        stream=wise.chat(prompt)
                    #response = st.write_stream(response_generator(' '.join(stream) )) 
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response, "avatar":"src\img\owl Open.png"})
            

