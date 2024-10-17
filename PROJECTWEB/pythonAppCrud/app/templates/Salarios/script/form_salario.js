document.addEventListener('DOMContentLoaded', function() {
    const anoMes = document.getElementById('id_mesAno');

    // Adiciona um listener para capturar a seleção
    anoMes.addEventListener('input', function() {
        console.log(anoMes.value); // Exibe o valor atual no console
    });
});