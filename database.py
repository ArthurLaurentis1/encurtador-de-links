"""
database.py: tudo que fala com o banco SQLite.

Funções para conectar, criar as tabelas (links e cliques), salvar um link,
buscar um link pelo código, registrar cliques e consultar estatísticas.
O SQL fica aqui para manter as rotas do main.py simples.

Partes deste código foram escritas com ajuda do Claude (IA da Anthropic),
conforme a regra de honestidade acadêmica do CS50. Explicação revisada por mim.
"""

import sqlite3

NOME_BANCO = "encurtador.db"

# Função que abre conexão com o banco
def conectar():
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabelas():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS links(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo INTERGER NOT NULL UNIQUE,
            url_original TEXT NOT NULL,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS cliques(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link_id INTEGER NOT NULL,
            data_hora TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (link_id) REFERENCES links (id)
        )
    """)

    # Grava de verdade as alterações no arquivo (sem isso, elas se perdem)
    conexao.commit() 
    # Fecha a conexão, já que terminamos de usar
    conexao.close()

def salvar_link(codigo, url_original):
    conexao = conectar()

    conexao.execute(
        "INSERT INTO links (codigo, url_original) VALUES (?, ?)",
        (codigo, url_original),
    )

    conexao.commit()
    conexao.close()

def buscar_link(codigo):
    conexao = conectar()

    linha = conexao.execute(
        "SELECT * FROM links WHERE codigo = ?",
        # A vírgula é obrigatória porque é uma tupla de um item só
        (codigo,),
    ).fetchone() # fetchone() pega só a primeira linha encontrada (ou None se não achar nenhuma)

    conexao.close()
    return linha

def registrar_clique(link_id):
    conexao = conectar()

    conexao.execute(
        "INSERT INTO cliques (link_id) VALUES (?)",
        (link_id,),
    )

    conexao.commit()
    conexao.close()

def contar_cliques(link_id):
    conexao = conectar()

    linha = conexao.execute(
        "SELECT COUNT(*) AS total FROM cliques WHERE link_id = ?",
        (link_id,),
    ).fetchone()

    conexao.close()
    return linha["total"]

def listar_links_com_cliques():
    conexao = conectar()

    linhas = conexao.execute("""
        SELECT links.id, links.codigo, links.url_original, links.criado_em,
            COUNT(cliques.id) AS total_cliques
        FROM links
            LEFT JOIN cliques ON cliques.link_id = links.id
        GROUP BY links.id
        ORDER BY links.id DESC
    """).fetchall()

    conexao.close()
    # Converte cada linha em dicionário comum e devolve a lista deles
    return [dict(linha) for linha in linhas]

def cliques_por_dia():
    conexao = conectar()

    linhas = conexao.execute("""
        SELECT DATE(data_hora, '-3 hours') AS dia,
            COUNT(*) AS total
        FROM cliques
        GROUP BY dia
        ORDER BY dia
    """).fetchall()

    conexao.close()
    return [dict(linha) for linha in linhas]

# Este bloco só roda quando executamos "python database.py" diretamente
if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas.")