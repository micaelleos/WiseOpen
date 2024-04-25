import streamlit as st
import time
from scripts.menu import menu_with_redirect, menu
from scripts.llm import motor_llm
import json

with open('config.json') as config_file:
    config = json.load(config_file)

api_key = config['api_key']

# Importando motor do wise
wise = motor_llm(api_key)

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("Wize Normas Open Finance")

initial_message = st.chat_message("assistant", avatar='src\img\owl Open.png')
initial_message.write("Olá, como posso ajudá-lo hoje?")  

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
        
        stream=wise.pergunta(prompt)
       
        #for m in stream:
        # response = st.write_stream([t for t in m.text])

        response = st.write_stream([m.text for m in stream])  
        #response = st.write(stream)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar":"src\img\owl Open.png"})
