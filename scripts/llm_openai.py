from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from scripts.databaseFunctions import vector_database
from langchain_community.callbacks import get_openai_callback


class OpenAI_chat:
    # Carregar variáveis de ambiente a partir de um arquivo .env
    load_dotenv()
    def __init__(self):
        self.llm_name = "gpt-3.5-turbo"
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.temepratura = 0.8
        self.llm = ChatOpenAI(model_name=self.llm_name,
                                temperature=self.temepratura,
                                openai_api_key=self.OPENAI_API_KEY,
                                streaming=True)
        self.custo = 0

        # Build prompt
        self.template = """
            Olá! vou explicar como você deve ser comportar.
            Você é um especialista em Open Finance Brasil. 
            Você deve auxiliar os usuários (instituições financeiras) a estar adequada as normativas do Bacen/BCB.
            Vou passar a você uma base de conhecimento a qual você deve utilizar para responder ao usuário.
            Caso seja necessário ou pedido pelo usuário ou sempre que possível, você deve informar qual normativa e qual localização onde pode ser encontrado a informação na normativa. Por exemplo: normativa IN441, sessão V, parágrafo 2
            Você deve dar orientações legais e tecnicas quanto ao cumprimento, boas práticas e descumprimento das normativas.
            Você deve dar informações completas, associado a resposta com diferentes pontos das normas.
            Para responder ao usuário, pense passo a passo.
            Dê sugestões ao usuário de como ele deve agir para obedecer as normativas, incluindo ações operacionais dentro da sua instituição.
            Use a seguinte base de conhecimento para responder a pergunta do usuário
            {context}
            Pergunta: {question}
            Resposta:"""
        self.QA_CHAIN_PROMPT = PromptTemplate.from_template(self.template)
        
        #init memory
        self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
                )  
        
        #get databse
        self.vectordb = vector_database()
        self.retriever = self.vectordb.as_retriever(search_type="mmr")
        
        #init chat
        self.qa = ConversationalRetrievalChain.from_llm(
            self.llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": self.QA_CHAIN_PROMPT}
        )

    def chat(self,question):
        with get_openai_callback() as custo:
            
            for response in self.qa({"question": question})['answer']:
                yield response
                
            self.custo_add(custo)
        
    def custo_add(self,custo):
        self.custo += custo.total_cost

