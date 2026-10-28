"""
main.py: arquivo principal da aplicação.

Cria o app FastAPI e define as rotas:
- página inicial e painel (HTML)
- criação de link curto
- redirecionamento (registrando o clique)
- dados de estatísticas para o gráfico

"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensagem": "Encurtador de links funcionando"}