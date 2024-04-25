### Passo a passo ###

 1) Instalar dependências:
        utilize o comando `pip install -r requirements.txt`
    
 2) Configurar API Gimini:
    O código foi criado baseado na api do ginimi. Siga os passos para tornar o código funcional com essa API:
       - 1) Crie uma chave do Gimini: Para criar uma chave para essa api vá em https://aistudio.google.com/app/apikey, gere a chave
       - 2) Na raiz do diretório do projeto, crie um arquivo chamado "config.json" e salve dentro dele:
            `{ "api_key": "sua_chave_de_api_aqui" }`
 4) Rodar projeto:
    Se você tiver Make instalado no computado, utilize o comando "make run"
    Caso contrário, utilize: `python -m streamlit run app.py`
