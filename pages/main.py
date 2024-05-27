import streamlit as st
import time
from scripts.menu import menu_with_redirect, menu
#from scripts.llm_gemini import Gemini_chat
from scripts.llm_openai import OpenAI_chat
import json
from streamlit_google_auth import Authenticate


# Show the navigation menu
menu_with_redirect()

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

st.title("Wize Normas Open Finance")

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
print(wise.custo)