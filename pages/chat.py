import streamlit as st
import time
from scripts.menu import menu_with_redirect, menu
#from scripts.llm_gemini import Gemini_chat
from scripts.llm_openai import OpenAI_chat
import json
from streamlit_google_auth import Authenticate
import types

st.set_page_config(initial_sidebar_state="collapsed")

lista_docs = ["doc1","doc2","doc3","doc4","doc5","doc6","doc7","doc8","doc9"]

st.markdown("""
    <style>
    .st-emotion-cache-13ln4jf {
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
    height : 40vh;
    }
    .st-emotion-cache-1clstc5 {
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    height : 33vh;
    overflow: auto;
    }
    .loader {
    width: 48px;
    height: 48px;
    border: 5px solid #FFF;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
    }
            
    .st-emotion-cache-1bzkvni{
    overflow: auto;
    }
            
    @keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
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

#st.markdown("""
#<span class="loader"></span>
#""", unsafe_allow_html=True)

# Show the navigation menu
menu_with_redirect()

def response_generator(response):
    for gen in response:
        yield gen 
        time.sleep(0.01)

def acumular_strings(generator):
    var = []
    for i in generator:
        next(var.append(i))
    return var

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.spinner(''):
    # Importando motor do wise
    #wise = Gemini_chat()
    wise = OpenAI_chat()


col=st.columns([0.3,0.7])
with st.container():
    with col[0]:
        with st.expander('Documentos para consulta',expanded=False):
            for item in lista_docs:
                with st.container(border=True):
                    st.checkbox(item)

        with st.expander('Chats',expanded=False):
            st.button("Novo chat",use_container_width=True)
            # Streamed response emulator


with st.container():
    with col[1]:
        st.header("Wize Normas Open Finance")
        with st.container(border=False):
            chat = st.container(height=400,border=False)
            with chat:
                initial_message = st.chat_message("assistant", avatar='src\img\owl Open.png')
                initial_message.write("Olá, como posso ajudá-lo hoje?")  
                
                messages = st.session_state.messages

                for i in range(0,len(messages)):
                    message = messages[i]

                    if i == len(messages)-1:
                        with st.chat_message(message["role"], avatar='src\img\owl Open.png'): 
                            
                            if isinstance(message["content"], types.GeneratorType):
                                resposta = st.write_stream(response_generator(message["content"])) 
                                message["content"] = str(resposta)
                                
                            else:
                                st.markdown(message["content"])             
                            
                            
                    else:
                        if message['role'] == "assistant":
                            with st.chat_message(message["role"], avatar='src\img\owl Open.png'):
                                st.markdown(message["content"])
                        else:
                            with st.chat_message(message["role"],avatar=st.session_state['user_info'].get('picture')):
                                st.markdown(message["content"])
                
            
            prompt = st.chat_input("Faça uma pergunta?",key="user_input")

            if prompt:
                
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                response=wise.chat(prompt)
                
                st.session_state.messages.append({"role": "assistant", "content": response})

                st.rerun()

