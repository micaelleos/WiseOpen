import streamlit as st
from scripts.menu import menu_with_redirect
import os
from langchain_community.document_loaders import PyPDFLoader
# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Repositório de normas")

uploaded_file = st.file_uploader("Escolha um arquivo PDF",type=['pdf'],accept_multiple_files=False)

def save_uploadedfile(uploadedfile):
    with open(os.path.join("uploads", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    

if uploaded_file is not None:
    st.success("Uploaded the file")
    save_uploadedfile(uploaded_file)

