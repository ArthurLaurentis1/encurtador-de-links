const tabela = document.getElementById("tabela-links");
const aviso = document.getElementById("aviso");

function criarCelula(texto){
    const celula = document.createElement("td");
    celula.textContent = texto;

    return celula;
}

function mostrarTabela(links) {
    tabela.textContent = "";

    if (links.length === 0 ) {
        aviso.textContent = "Nenhum link criado ainda.";
        return;
    }

    for (const link of links){
        const linha = document.createElement("tr");
        
        // Converte a data do banco (UTC) para o horário do navegador
        // O replace troca o espaço por "T" e o "Z" no fim indica UTC
        const data = new Date(link.criado_em.replace(" ", "T") + "Z");
        
        linha.appendChild(criarCelula(link.codigo));

        const celulaUrl = criarCelula(link.url_original);
        celulaUrl.className = "url";
        celulaUrl.title = link.url_original;
        
        linha.appendChild(celulaUrl);
        linha.appendChild(criarCelula(data.toLocaleDateString("pt-br")));
        linha.appendChild(criarCelula(link.total_cliques));

        tabela.appendChild(linha);
    }
}

async function carregarDados() {
    try {
        // Faz um pedido GET (padrão do fetch) para a rota de estatísticas
        const resposta = await fetch("/api/estatisticas");

        if (!resposta.ok) {
            aviso.textContent = "Não foi possível carregar as estatísticas.";
            return;
        }

        // Converte a resposta em objeto JavaScript
        const dados = await resposta.json();

        // Desenha a tabela com a lista "links" que veio do Python
        mostrarTabela(dados.links);
    } catch (erro) {
        aviso.textContent = "Não foi possível conectar ao servidor.";
    }
}
carregarDados();