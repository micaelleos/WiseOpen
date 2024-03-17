import streamlit as st
import google.generativeai as genai
import time
from scripts.menu import menu_with_redirect, menu
from scripts.llm import motor_llm

# Importando motor do wise
wise = motor_llm(genai)

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("Wize Normas Open Finance")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Faça uma pergunta?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar='src\img\owl Open.png'):
        stream=wise.chat.send_message(prompt, stream=True)
       
        #for m in stream:
        # response = st.write_stream([t for t in m.text])

        response = st.write_stream([m.text for m in stream])  
        #response = st.write(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
