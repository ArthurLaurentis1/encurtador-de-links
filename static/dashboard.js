const tabela = document.getElementById("tabela-links");
const aviso = document.getElementById("aviso");
const avisoGrafico = document.getElementById("aviso-grafico");

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

function mostrarGrafico(cliquesPorDia) {
    if (cliquesPorDia.length === 0) {
        avisoGrafico.textContent = "Ainda não há cliques para mostrar.";
        return;
    }

    // O .map cria uma lista nova aplicando a função a cada item da lista original
    const rotulos = cliquesPorDia.map(function(item) {
        // Troca "2026-10-28" por "28/10/2026"
        return item.dia.split("-").reverse().join("/");
    });

    const valores = cliquesPorDia.map(function(item){
        return item.total;
    });

    const canvas = document.getElementById("grafico-cliques");

     // Cria o gráfico; "new Chart" vem da biblioteca Chart.js
    new Chart(canvas, {
        type: "bar",
        data: {
            labels: rotulos,
            datasets: [{
                label: "Cliques por dia",
                data: valores,
            }],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 },
                },
            },
        },
    });
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
        mostrarGrafico(dados.cliques_por_dia);
    } catch (erro) {
        aviso.textContent = "Não foi possível conectar ao servidor.";
    }
}
carregarDados();