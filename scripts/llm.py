import google.generativeai as genai
from scripts.databaseFunctions import retrive_context_db, retrive_context_txt
import logging

class motor_llm:

  def __init__(self,api_key):
    self.api = genai
    self.api.configure(api_key=api_key)
    self.contexto = retrive_context_txt()
    self.system_prompt =f"""
    Olá! vou explicar como você deve ser comportar.
    Você é um especialista em Open Finance Brasil. 
    Você deve auxiliar os usuários (instituições financeiras) a estar adequada as normativas do Bacen/BCB.
    As perguntas dos usuários serão delimitadas por ###.
    Vou passar a você uma base de conhecimento a qual você deve utilizar para responder ao usuário.
    Caso seja necessário ou pedido pelo usuário ou sempre que possível, você deve informar qual normativa e qual localização onde pode ser encontrado a informação na normativa. Por exemplo: normativa IN441, sessão V, parágrafo 2
    Você deve dar orientações legais e tecnicas quanto ao cumprimento, boas práticas e descumprimento das normativas.
    Você deve dar informações completas, associado a resposta com diferentes pontos das normas.
    Para responder ao usuário, pense passo a passo.
    Dê sugestões ao usuário de como ele deve agir para obedecer as normativas, incluindo ações operacionais dentro da sua instituição.
    """
    self.assistant_prompt =f"""
    Para responder ao usuário, considere a seguinte base de conhecimento delimitada por ```:
    ```{self.contexto}```
    """
  
    # Set up the model
    self.generation_config = {
      "temperature": 0.8,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }

    self.safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    self.model = self.api.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=self.generation_config,
                                  safety_settings=self.safety_settings)

    self.chat = self.model.start_chat(history=[
    {
      "role": "user",
      "parts": [self.system_prompt]
    },
        {
      "role": "model",
      "parts": ["Ok!"]
    },
    {
      "role": "user",
      "parts": [self.assistant_prompt]
    },
    {
      "role": "model",
      "parts": ["Olá! como posso ajudá-lo hoje?"]
    },
    ])

  def pergunta_com_contexto(self,query):
    self.base_conhecimento = retrive_context_db(query)
    self.prompt=f"""
    Dado que: {self.base_conhecimento}
    O usuário gostaria de saber o seguinte: ###{query}###
    """
    logging.info(self.prompt)
    print(self.prompt)
    stream=self.chat.send_message(self.prompt, stream=True)

    return stream

  def pergunta(self,query):
    self.query_delimitada = f"###{query}###"
    stream=self.chat.send_message(self.query_delimitada, stream=True)
    return stream


