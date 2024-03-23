# This peace of code load the files in directory to the database
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
persist_directory="./chroma_db"

def listar_documentos_caminho(pasta) -> list:
    '''Retorna lista de arquivos dentro do diretório'''
    documentos = []

    # Percorre todos os arquivos e pastas no caminho fornecido
    for item in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, item)
        
        # Verifica se é um arquivo
        if os.path.isfile(caminho_completo):
            documentos.append(caminho_completo)
    
    return documentos

def load_context():
    '''Faz o load do PDF no banco de dados'''
    lista = listar_documentos_caminho("./uploads/")

    if lista:
        for item in lista:
            # load the document and split it into chunks
            loader = PyPDFLoader(item)
            documents = loader.load()
            
            # split it into chunks
            text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            docs = text_splitter.split_documents(documents)

            # load it into Chroma
            Chroma.from_documents(docs, embedding_function, persist_directory=persist_directory)
            os.remove(item)

def retrive_context(query:str)->list:
    '''Faz query de similaridade na banco de dados e retorna chuncks mais similares'''

    vectordb = Chroma(persist_directory=persist_directory, 
                    embedding_function=embedding_function)
    
    retriever = vectordb.as_retriever()
    docs = retriever.get_relevant_documents(query)
    
    return docs

if __name__ == "__main__":
    #load_context()
    docs = retrive_context('Qual deve ser a disponibilidade de uma API?')
    for i in docs:
        print(i)
        print('---------------------------------------------------------------------------------')