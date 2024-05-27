# This peace of code load the files in directory to the database
import os
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

# Carregar variáveis de ambiente a partir de um arquivo .env
load_dotenv()

# create the open-source embedding function
persist_directory="./chroma_db"

embedding = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

def load_to_database(documents,chunk_size=500,chunk_overlap=50):
    '''Faz o load do docs no banco de dados'''

    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""]
    )

    if documents:
        for item in documents:
            splits = r_splitter.split_documents(item)
            
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

def retrive_context_db(query:str)->list:
    '''Faz query de similaridade na banco de dados e retorna chuncks mais similares'''

    vectordb = Chroma(persist_directory=persist_directory, 
                    embedding_function=embedding)
    
    retriever = vectordb.as_retriever()
    docs = retriever.get_relevant_documents(query)
    return docs

def vector_database():
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return db

if __name__ == "__main__":
    from documents_loaders import preprocessing_docs
    vectordb = load_to_database(preprocessing_docs('uploads'))
    print(vectordb._collection.count())

    