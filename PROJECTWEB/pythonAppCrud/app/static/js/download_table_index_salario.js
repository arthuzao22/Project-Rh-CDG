function baixarExcel() {
    const tabela = document.getElementById("indexsalario");
    let csv = [];
    const linhas = tabela.querySelectorAll("tr");

    // Iterar sobre cada linha da tabela (tanto cabeçalho quanto dados)
    for (let i = 0; i < linhas.length; i++) {
        let cols = linhas[i].querySelectorAll("td, th");
        let linha = [];
        for (let j = 0; j < cols.length; j++) {
            linha.push(cols[j].innerText);
        }
        csv.push(linha.join(","));
    }

    // Criar o conteúdo CSV como string
    let csvString = csv.join("\n");

    // Criar um Blob com os dados CSV
    let blob = new Blob([csvString], { type: 'text/csv' });

    // Criar um link temporário para download
    let link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "tabela.csv";  // Nome do arquivo
    link.style.display = "none";

    // Adicionar o link ao documento e clicar nele para baixar
    document.body.appendChild(link);
    link.click();

    // Remover o link após o download
    document.body.removeChild(link);
}



