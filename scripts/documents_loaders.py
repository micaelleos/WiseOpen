from langchain.document_loaders import PyPDFLoader
import os
import re

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

def load_documents(upload_dir) -> list:
    '''Faz o load do PDF no banco de dados'''
    lista = listar_documentos_caminho(upload_dir)

    documents = []
    if lista:
        for item in lista:
            # load the document and split it into chunks
            file = PyPDFLoader(item)
            doc = file.load()

            rm=[]
            for i in range(0,len(doc)):
                if not doc[i].page_content:
                   rm.append(doc[i]) 
            
            for m in rm:
                doc.remove(m)

            if not doc:
                raise ValueError("O arquivo está vazio.")
            
            documents.append(doc)
            
            return documents      
    

def preprocessing_docs(upload_dir):
    "Faz validações e limpezas no arquivo"
    try:
        documents = load_documents(upload_dir)

        # limpeza de arquivo
        pattern_x00 = re.compile(r'\x00') 
        pattern_n = re.compile(r'\n')
        for pages in documents:
            for i in range(0,len(pages)):
                pages[i].page_content = pattern_x00.sub('ti', pages[i].page_content)
                pages[i].page_content = pattern_n.sub(' ', pages[i].page_content)

        return documents
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Não foi encontrado arquivo em '{upload_dir}'.")
    except ValueError as e:
        print(f"Erro: {e}")
        raise
    

if __name__ == "__main__":
    docs = preprocessing_docs('uploads')
    #docs = load_documents('uploads')
    print(docs)