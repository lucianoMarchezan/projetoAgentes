var linhaMatriz = 10;
var colunaMatriz = 10;

const mensagens = {
    ID_CASA: 0,
    ID_PROXIMA_CASA: 1,
    AGENTE: 2,
    STATE_CASA: 3,
    STATE_PROXIMA_CASA: 4
}

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
            casa.innerHTML = ""+i + j
            matrizLocal.push(casa);
            matrizGUI.appendChild(casa);
        }

        matrizGUI.appendChild(quebraLinha);
    }
}


require('electron').ipcRenderer.on('mudaCor', (event, message) => {
    let casa = document.getElementById(message);

    casa.className = "col casa casaChamas";
})

require('electron').ipcRenderer.on('apagarFogo', (event, message) => {
    let casa = document.getElementById(message);

    casa.className = "col casa";
})


require('electron').ipcRenderer.on('andar', (event, message) => {
    let casaAtual = document.getElementById(message[mensagens.ID_CASA]);
    let proximaCasa = document.getElementById(message[mensagens.ID_PROXIMA_CASA]);
    let agente = document.createElement("div");

    if(message[mensagens.STATE_PROXIMA_CASA] == "Vazio"){
        console.log()
        proximaCasa.appendChild(agente);
        agente.innerHTML = '<h3> ' + message[mensagens.AGENTE] + ' <h3>';
        
        if(message[mensagens.AGENTE] == 'Civil'){
            proximaCasa.className = "col casa casaCivil";
        }else if(message[2] == 'Bombeiro'){
            proximaCasa.className = "col casa casaBombeiro";
        }
    }

    console.log(message[mensagens.STATE_CASA])
    if(message[mensagens.STATE_CASA] == message[mensagens.AGENTE]){
        casaAtual.className = "col casa";
        casaAtual.innerHTML = message[mensagens.ID_CASA];
    }

});

require('electron').ipcRenderer.on('posicaoInicial', (event, message) => {
    let casaAtual = document.getElementById(message);
    let bombeiro = document.createElement("div");

    bombeiro.innerHTML = '<h3> B <h3>';
    casaAtual.innerHTML = message;
    casaAtual.className = "col casa";
    proximaCasa.appendChild(bombeiro);
    proximaCasa.className = "col casa casaBombeiro";

});