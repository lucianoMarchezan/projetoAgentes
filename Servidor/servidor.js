const express = require('express');//Biblioteca express para criar o servidor
const bodyParser = require('body-parser');
const app = express();//Instancia do express para ser utilizada para criar o servidor
var win;


app.use(bodyParser.json());

app.post('/AgenteTeste', (req, res) => {
    ordem = req.body;

    if(ordem.tipoMensagem == "mudaCor"){
        win.webContents.send('mudaCor', ordem.mensagem);
    }

    res.send('Mensagem recebida');
  });

app.listen(9000, function () {
    console.log('Cenário Escutando na porta 9000!');
    
});

module.exports = {
    setWindow: (janela) =>{
        win = janela;
    }
};