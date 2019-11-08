var linhaMatriz = 10;
var colunaMatriz = 10;


function criarMatriz() {
    let matrizGUI = document.getElementById("matriz");
    let matrizLocal = new Array();

    for (let i = 0; i < linhaMatriz; i++) {
        let quebraLinha = document.createElement("div");
        quebraLinha.className = "w-100"

        for (let j = 0; j < colunaMatriz; j++) {
            let casa = document.createElement("div");
            casa.id = "" + i + j
            casa.className = "col casa";
            casa.innerHTML = "Linha " + i + " Coluna " + j
            matrizLocal.push(casa);
            matrizGUI.appendChild(casa);
        }

        matrizGUI.appendChild(quebraLinha);
    }
}


require('electron').ipcRenderer.on('mudaCor', (event, message) => {
    let casa = document.getElementById(message);

    casa.style.backgroundColor = "red";
})