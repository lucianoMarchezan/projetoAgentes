var linhaMatriz = 10;
var colunaMatriz = 10;
var matriz = null;
let socket = new WebSocket("ws://127.0.0.1:8080");



function criarMatriz() {
    let matrizGUI = document.getElementById("matriz");
    let matrizLocal = new Array();

    for (let i = 0; i < linhaMatriz; i++) {
        let quebraLinha = document.createElement("div");
        quebraLinha.className = "w-100"

        for (let j = 0; j < colunaMatriz; j++) {
            let casa = document.createElement("div");
            casa.id = ""+i+j
            casa.className = "col casa";
            casa.innerHTML = "Linha " + i + " Coluna " + j
            matrizLocal.push(casa);
            matrizGUI.appendChild(casa);
        }

        matrizGUI.appendChild(quebraLinha);
    }

    matriz = matrizGUI;
}



socket.onopen = function (e) {
    alert("[open] Connection established");
};

socket.onmessage = function (event) {
    mensagem = JSON.parse(event.data);
    
    if (mensagem.tipoMensagem == "mudaCor") {
        mudaCor(mensagem.mensagem);
    }
};

socket.onclose = function (event) {
    if (event.wasClean) {
        alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        alert('[close] Connection died');
    }
};

function testar() {
    let obj = {
        "tipoMensagem": "update GUI",
        "teste": "dsadsa"
    };
    socket.send(JSON.stringify(obj));
}

function testar2() {
    let obj = {
        "tipoMensagem": "teste",
        "teste": "dsadsa"
    };
    socket.send(JSON.stringify(obj));
}

function mudaCor(id) {
    let casa = document.getElementById(id);

    casa.style.backgroundColor = "red";
}