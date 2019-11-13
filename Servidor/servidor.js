const express = require('express'); //Biblioteca express para criar o servidor
const bodyParser = require('body-parser');
const app = express(); //Instancia do express para ser utilizada para criar o servidor
const shell = require('child_process');
var win;
var linhaMatriz = 10;
var colunaMatriz = 10;
var matriz;

app.use(bodyParser.json());

app.post('/Incendiario', (req, res) => {
    ordem = req.body;
    let casa, linha, coluna;

    if (ordem.tipoMensagem == "mudaCor") {
        linha = ordem.mensagem.charAt(0);
        coluna = ordem.mensagem.charAt(1);
        casa = matriz[linha][coluna];

        casa.state = "Fogo";
        win.webContents.send('mudaCor', ordem.mensagem);
    }

    res.send('Mensagem recebida');
});

app.post('/PosicaoInicial', (req, res) => {
    let ordem = req.body;
    let casa = JSON.parse(ordem.casaAtual);
    let state = ordem.state;
    let listaOrdem = new Array();


    casa = matriz[casa.linha][casa.coluna]
    listaOrdem.push(casa);
    listaOrdem.push(ordem.state);

    if (casa.state == "Vazio") {
        casa.state = state;
        win.webContents.send('posicaoInicial', listaOrdem);
        res.send("Movimento bem-sucedido!");
    }

});

app.post('/Andar', (req, res) => {
    ordem = req.body;

    if (ordem.tipoMensagem == "andar") {
        let casa = JSON.parse(ordem.casaAtual);
        let proximaCasa = JSON.parse(ordem.proximaCasa);
        let casas = new Array();

        casa = matriz[casa.linha][casa.coluna]
        proximaCasa = matriz[proximaCasa.linha][proximaCasa.coluna]
        casas.push(casa.nameId);
        casas.push(proximaCasa.nameId);
        casas.push(ordem.state)
        casas.push(casa.state)
        casas.push(proximaCasa.state)

        if (proximaCasa.state == "Vazio") {
            proximaCasa.state = ordem.state;
        }

        if (casa.state == ordem.state) {
            casa.state = "Vazio";
        }

        win.webContents.send('andar', casas);
        res.send("Movimento bem-sucedido!");
    }
});



app.post('/ApagarFogo', (req, res) => {
    let casa = req.body;

    casa = matriz[casa.linha][casa.coluna]

    if (casa.state == "Fogo") {
        casa.state = "Vazio";
        win.webContents.send('apagarFogo', casa).nameId;
        res.send("Fogo Apagado!");
    }
});


////Comandos Civil/////

app.post('/VerificarCasa', (req, res) => {
    ordem = req.body;

    if (ordem.tipoMensagem == "verificarCasa") {
        let casa = JSON.parse(ordem.mensagem);
        let casaRetorno = matriz[casa.linha][casa.coluna]
        res.send(JSON.stringify(casaRetorno));
    }
});
////Fim Comandos Civil/////


///Comando iNcendiario///
app.post('/VerificarCasaIncendiario', (req, res) => {

    ordem = req.body;

    if (ordem.tipoMensagem == "verificarCasaIncediario") {
        let casa = JSON.parse(ordem.mensagem);
        let casaRetorno = matriz[casa.linha][casa.coluna]
        res.send(JSON.stringify(casaRetorno));
    }
});

app.listen(9000, function() {
    console.log('Cenário Escutando na porta 9000!');
    criarMatriz();
    abrirProcessoAgentes();
});

//Abre o processo de agentes
function abrirProcessoAgentes() {
    let comandos = "cd ../Projeto Python && " +
        "python main.py";
    let child;

    child = shell.spawn(comandos, { shell: true });

    child.stderr.on('data', function(data) {
        console.error("STDERR:", data.toString());
    });
    child.stdout.on('data', function(data) {
        console.log("STDOUT:", data.toString());
    });
    child.on('exit', function(exitCode) {
        console.log("Child exited with code: " + exitCode);
    });
}

function criarMatriz() {
    let novaMatriz = new Array();

    for (let i = 0; i < linhaMatriz; i++) {
        let linhas = new Array();
        for (let j = 0; j < colunaMatriz; j++) {
            let casa = {
                "nameId": '' + i + j,
                "state": 'Vazio',
                "linha": i,
                "coluna": j
            }
            linhas.push(casa);
        }
        novaMatriz.push(linhas);
    }

    matriz = novaMatriz;
}

module.exports = {
    setWindow: (janela) => {
        win = janela;
    }
};