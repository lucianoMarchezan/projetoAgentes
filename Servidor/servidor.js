const express = require('express');//Biblioteca express para criar o servidor
var bodyParser = require('body-parser');
const SocketServer = require('ws').Server;
const path = require('path');
const PORT = process.env.PORT || 8080;
const INDEX = path.join(__dirname, 'index.html');
const app = express();//Instancia do express para ser utilizada para criar o servidor
const server = express()
    .use((req, res) => res.sendFile(INDEX))
    .listen(PORT, () => console.log(`Listening on ${PORT}`));

const wss = new SocketServer({ server });
var wsGUI;



wss.on('connection', (ws) => {

    console.log('Client connected');
    wsGUI = ws;

    //Vai lidar com qualquer mensagem que o servidor
    //receber através de sockets
    ws.on('message', function (message) {
        let desafio;
        let localArquivo;

        lidaComMensagem(message, ws);
    });

    //Lida com fechamento de uma conexão feita por um cliente
    ws.on('close', function (connection) {
        console.log("Cliente Saiu");
    });

});

//Método existe só para manter a conexão com os clientes viva
setInterval(() => {

    wss.clients.forEach((client) => {

        client.send(new Date().toTimeString());

    });

}, 10000);

function lidaComMensagem(mensagem, ws) {
    console.log(mensagem);
    var objeto = JSON.parse(mensagem);

    try {
        if(objeto.tipoMensagem == "update GUI"){
            ws.send(JSON.stringify(criaJson()));
        }else if(objeto.tipoMensagem == "teste"){
            ws.send(JSON.stringify(criaJson("mudaCor", "35")));
        }
    } catch (error) {
        console.log(error);
        return null;
    }

    return null;
}


function criaJson(tipoMensagem, mensagem, mensagemResultado) {
    if (tipoMensagem == "Resultado Jogador") {
        return {
            "tipoMensagem": tipoMensagem,
            "mensagem": mensagem,
            "mensagemResultado": mensagemResultado
        }
    } else {
        return {
            "tipoMensagem": tipoMensagem,
            "mensagem": mensagem
        }
    }
}


app.use(express.static("web-desktop"));
app.use(bodyParser.json());

app.post('/AgenteTeste', (req, res) => {
    ordem = req.body

    if(ordem.tipoMensagem == "mudaCor"){
        wsGUI.send(JSON.stringify(criaJson("mudaCor", ordem.mensagem)));
    }

    res.send('Hello from App Engine!');
  });

app.listen(9000, function () {
    console.log('App de Exemplo escutando na porta 9000!');
});