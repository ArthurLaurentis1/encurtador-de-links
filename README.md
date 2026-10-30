# Encurtador de Links

Video Demo: <COLE AQUI A URL DO VÍDEO>

## Descrição

Este é um encurtador de links com painel de estatísticas, feito como projeto final do CS50x. A pessoa cola uma URL longa e recebe um link curto. Cada vez que alguém abre esse link curto, o clique fica registrado, e uma página de painel mostra todos os links criados, quantos cliques cada um recebeu e um gráfico de cliques por dia.

Escolhi esse tema porque ele junta quase tudo que aprendi no curso (Python, SQL, HTML, CSS e JavaScript) em algo pequeno que funciona de ponta a ponta. Também quis aprender uma ferramenta nova, então usei FastAPI no lugar do Flask dos psets.

## Como funciona

**Criar um link.** Na página inicial, o JavaScript envia a URL com `fetch` para a rota `POST /encurtar`. O servidor confere se ela começa com `http://` ou `https://`, gera um código aleatório de 6 caracteres (letras e números), garante que ele ainda não existe no banco, salva e devolve o link curto.

**Acessar um link.** Quando alguém abre `/<código>`, o servidor procura o código no banco. Se não encontra, responde 404. Se encontra, registra um clique e redireciona o navegador para a URL original.

**Ver as estatísticas.** A página `/dashboard` pede os dados à rota `/api/estatisticas`, que devolve JSON. Com eles, o `dashboard.js` monta a tabela de links e um gráfico de barras com Chart.js.

## Arquivos do projeto

- `main.py`: cria o app FastAPI e define as rotas (página inicial, painel, criação do link, redirecionamento e estatísticas).
- `database.py`: tudo que fala com o SQLite. Cria as tabelas e tem as funções de salvar link, buscar link, registrar clique, contar cliques e gerar as estatísticas. Mantive o SQL aqui para as rotas ficarem simples.
- `templates/index.html` e `templates/dashboard.html`: as duas páginas, renderizadas com Jinja2.
- `static/app.js`: envia a URL ao servidor e mostra o link curto sem recarregar a página.
- `static/dashboard.js`: busca as estatísticas e desenha a tabela e o gráfico.
- `static/style.css`: o visual das duas páginas.
- `requirements.txt`: as bibliotecas necessárias (fastapi, uvicorn e jinja2).

## Decisões de projeto

**FastAPI.** Gostei de duas coisas: ele valida o formato dos dados que chegam (com Pydantic) sem eu escrever vários `if`, e gera sozinho uma documentação testável em `/docs`, que usei muito durante o desenvolvimento.

**SQLite.** Para um projeto desse tamanho, um banco em arquivo único, sem servidor para instalar, é suficiente. Usei o módulo `sqlite3` do Python direto, em vez da biblioteca do CS50, para entender melhor o que acontece por baixo.

**Duas tabelas.** `links` guarda o código e a URL original. `cliques` guarda só o `link_id` e a data e hora. Assim não repito a URL a cada clique, e consigo contar cliques por link e por dia. Na listagem usei `LEFT JOIN` e `COUNT(cliques.id)` para que links sem nenhum clique também apareçam, com zero.

**Redirecionamento 302 e não 301.** O 301 é guardado em cache pelo navegador, e os cliques seguintes nem chegariam ao servidor para serem contados.

**Segurança básica.** Uso `?` nas consultas SQL para evitar SQL injection, `secrets` para gerar os códigos (mais difícil de adivinhar que o `random`) e `textContent` em vez de `innerHTML` no JavaScript, para que uma URL maliciosa não vire código na página.

**Fuso horário.** O SQLite guarda a hora em UTC. No gráfico, ajusto -3 horas na própria consulta SQL, e na tabela o navegador converte para o horário local.

## Como rodar

Com Python instalado, na pasta do projeto:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Depois abra `http://127.0.0.1:8000`. O painel fica em `/dashboard`. O banco (`encurtador.db`) é criado sozinho na primeira execução. No Linux ou macOS, a ativação do ambiente virtual é `source venv/bin/activate`.

## Limitações e melhorias futuras

- O painel não tem login: qualquer pessoa com o endereço vê todos os links.
- O projeto roda só localmente. Para publicar, seria preciso escolher uma hospedagem que mantenha o arquivo do SQLite, e só com um domínio curto o link ficaria realmente curto.
- O gráfico usa o Chart.js por CDN, então precisa de internet.
- Ideias para o futuro: links que expiram, apelidos personalizados e separar cliques repetidos da mesma pessoa.

## Uso de IA

Seguindo a regra de honestidade acadêmica do CS50, informo que usei o Claude (Anthropic) como apoio. Ele ajudou a planejar a estrutura, escreveu trechos de código com explicação linha por linha e me ajudou a depurar erros. Todos os arquivos têm um comentário no topo registrando isso.
Eu testei cada etapa, fiz perguntas sobre cada trecho até entender e corrigi problemas pelo caminho.