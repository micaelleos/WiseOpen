import streamlit as st
from scripts.menu import menu_with_redirect

menu_with_redirect() # Render the dynamic menu!

st.markdown('''## Bem-vindo à nossa Plataforma de Busca Normativa do Banco Central! 
Sua fonte definitiva para encontrar informações normativas relevantes do Banco Central do Brasil de maneira rápida e eficiente.
### Como Funciona:

1. **Pergunte ao Wize:** Utilize nossa ferramenta de busca intuitiva para fazer perguntas sobre normas do Banco Central. Nosso assistente virtual está pronto para fornecer respostas precisas e relevantes para suas consultas.

2. **Upload de Novas Normas:** Você também tem a oportunidade de contribuir para o aprimoramento da nossa base de dados. Faça o upload de novas normas e regulamentações diretamente na plataforma. Nosso wizard aprenderá com elas, tornando-se cada vez mais inteligente e capaz de oferecer respostas ainda melhores.

### Por que Usar Nossa Plataforma:

- **Eficiência:** Não perca mais tempo procurando informações normativas manualmente. Nossa plataforma oferece resultados instantâneos e precisos para suas consultas.

- **Atualizações Constantes:** Mantemos nossa base de dados sempre atualizada com as últimas normas e regulamentações do Banco Central, garantindo que você tenha acesso às informações mais recentes.

- **Contribuição Colaborativa:** Ao fazer o upload de novas normas, você contribui para a melhoria contínua da nossa plataforma, tornando-a ainda mais útil para todos os usuários.

Comece a explorar nossa Plataforma de Busca Normativa agora e simplifique sua pesquisa por informações do Banco Central!'''
)

