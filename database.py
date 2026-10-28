"""
database.py: tudo que fala com o banco SQLite.

Funções para conectar, criar as tabelas (links e cliques), salvar um link,
buscar um link pelo código, registrar cliques e consultar estatísticas.
O SQL fica aqui para manter as rotas do main.py simples.

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

# Este bloco só roda quando executamos "python database.py" diretamente
if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas.")