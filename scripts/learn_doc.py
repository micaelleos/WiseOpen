from scripts.documents_loaders import listar_documentos_caminho, preprocessing_docs
import shutil
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter


def learn_docs(dir_processed, dir_upload, model:list='gemini'):
    if not os.path.exists(dir_processed):
        os.makedirs(dir_processed)

    docs = preprocessing_docs(dir_upload)

    r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=0,
    separators=["\n\n", "\n", "(?<=\. )", " ", ""]
    )

    for item in docs:
        splits = r_splitter.split_documents(item)

    chat_context = []
    if model == 'gemini':
        for info in splits:
            chat_context.append(
                {
                "role": "user",
                "parts": [f"{info}"]
                })
            chat_context.append(
                {
                "role": "model",
                "parts": ["Ok!"]
                }
                )

    # move arquivos para diretório de arquivos processados
    files = listar_documentos_caminho(dir_upload)
    for file in files:
        shutil.move(file, dir_processed)

    return chat_context

if __name__ == "__main__":
    chat = learn_docs("uploads/processed", "uploads/stage", model='gemini')
    print(chat)