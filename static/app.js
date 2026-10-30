const formulario = document.getElementById("formulario");
const campoUrl = document.getElementById("campo-url");
const resultado = document.getElementById("resultado");

formulario.addEventListener("submit", async function(evento) {
    // Impede o comportamento padrão do formulário, que seria recarregar a página
    evento.preventDefault(); 

    resultado.textContent = "Encurtando...";

    try {
        const resposta = await fetch("/encurtar", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({ url: campoUrl.value.trim()
        })
    });

        const dados = await resposta.json();

        if(!resposta.ok){
            resultado.textContent =
                "Erro: " + (typeof dados.detail === "string" ? dados.detail :"URL inválida");
            return;
        }

        const link = document.createElement("a");
        link.href = dados.link_curto;
        link.textContent = dados.link_curto.replace("http://", "").replace("https://", "");
        link.target = "_blank";

        resultado.textContent = "Seu link curto: ";
        resultado.appendChild(link)
    } catch (erro){
        console.error(erro);
        resultado.textContent = "Não foi possível conectar ao servidor.";
    }

    console.log(dados);
});