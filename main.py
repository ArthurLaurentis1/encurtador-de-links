"""
main.py: arquivo principal da aplicação.

Cria o app FastAPI e define as rotas:
- página inicial e painel (HTML)
- criação de link curto
- redirecionamento (registrando o clique)
- dados de estatísticas para o gráfico

"""

import secrets                                                          # Módulo para gerar números aleatórios seguros
import string                                                           # Módulo com listas prontas de letras e números
from fastapi import FastAPI, HTTPException, Request                     # FastAPI cria o app; HTTPException devolve erros; Request representa o pedido recebido
from fastapi.staticfiles import StaticFiles                             # Permite servir arquivos prontos (CSS, JavaScript) de uma pasta
from fastapi.templating import Jinja2Templates                          # Permite montar páginas HTML a partir de templates (usa o Jinja2)
from fastapi.responses import HTMLResponse, RedirectResponse            # HTMLResponse indica que a resposta é uma página; RedirectResponse redireciona
from pydantic import BaseModel                                          # BaseModel define o formato dos dados que o navegador envia
import database                                                         # Importa o nosso arquivo database.py para usar as funções do banco


app = FastAPI()

# Diz que tudo que começar com /static/ vem dos arquivos da pasta "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diz que os templates HTML ficam na pasta "templates"
templates = Jinja2Templates(directory="templates")

# Garante que as tabelas existem sempre que o servidor iniciar
database.criar_tabelas()

# Caracteres permitidos no código curto: letras (maiúsculas e minúsculas) e números
ALFABETO = string.ascii_letters + string.digits

class PedidoEncurtar(BaseModel):
    url: str

def gerar_codigo(tamanho = 6):
    return "".join(secrets.choice(ALFABETO) for i in range(tamanho))
    # Gera e sorteia codigos aleatorios

# Rota da página inicial, response_class avisa que a resposta é HTML
@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    # Lê o arquivo templates/index.html e devolve como página
    return templates.TemplateResponse(request=request, name="index.html")

# Rota que recebe uma URL e devolve o link curto; usa POST porque envia dados
@app.post("/encurtar")
def encurtar(pedido: PedidoEncurtar):
    url = pedido.url.strip() # Pega a url enviada e remove espaços

    # Se a url não começar com http:// ou https://, não é um endereço válido
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="A URL deve começar com http:// ou https://")

    codigo = gerar_codigo()

    while database.buscar_link(codigo) is not None:
        codigo = gerar_codigo()
    # Enquanto já existir um link com esse código no banco... gera outro código, até achar um que esteja livre

    database.salvar_link(codigo, url)

    # Devolve o código e o link curto completo
    return {"codigo": codigo, "link_curto": f"http://127.0.0.1:8000/{codigo}"}

# Rota que devolve os dados do painel em JSON (o dashboard.js vai buscar isso)
@app.get("/api/estatisticas")
def estatisticas():

    # Devolve um dicionário com as duas listas; o FastAPI converte para JSON
    return{
        # Lista de links com o total de cliques de cada um
        "links": database.listar_links_com_cliques(),
        # Lista de dias com o total de cliques de cada dia
        "cliques_por_dia": database.cliques_por_dia(),
    }

@app.get("/{codigo}")
def redirecionar(codigo: str):
    link = database.buscar_link(codigo) # Procura no banco o link que tem esse código

    if link is None:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    database.registrar_clique(link["id"])

    # Manda o navegador para a URL original; 302 significa "redirecionamento temporário"
    return RedirectResponse(url=link["url_original"], status_code=302)