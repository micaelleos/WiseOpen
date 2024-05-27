import streamlit as st
from scripts.menu import menu_with_redirect
import os
from langchain_community.document_loaders import PyPDFLoader
from scripts.documents_loaders import preprocessing_docs
from scripts.databaseFunctions import load_to_database
import shutil


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Repositório de normas")

UPLOAD_DIR = "uploads"

uploaded_file = st.file_uploader("Escolha um arquivo PDF",type=['pdf'],accept_multiple_files=False)

def save_uploadedfile(uploadedfile):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    with open(os.path.join(UPLOAD_DIR, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    

if uploaded_file is not None:
    with st.spinner('Uploading file...'):
        save_uploadedfile(uploaded_file)
    
    try:
        with st.spinner('Preprocessing file...'):
                documents = preprocessing_docs(UPLOAD_DIR)
        with st.spinner('Saving file in database...'):
            load_to_database(documents)
            shutil.rmtree(UPLOAD_DIR)

        st.success("File saved in database")

    except ValueError as e:
        st.error("O documento está vazio (não possui caracteres). Por favor, faça um novo upload.")
    



