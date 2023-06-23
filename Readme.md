# NF-e Ouro (Nota Fiscal Eletrônica do Ouro)

Este é um repositório de exemplo, em Python 3, de integração da Nota Fiscal Eletrônica do Ouro com os serviços disponibilizados pela respectiva API.

## Dependências

As dependências para este projeto encontram-se no arquivo [requirements.txt](requirements.txt). </br></br>
Solicita-se atenção com relação à biblioteca signxml. Nos testes com a versão 3.2.0, o valor das assinaturas (*SignatureValue*) com o algoritmo RSA-SHA1 era diferente do esperado pelo serviço, sendo que o *DigestValue* permaneceu igual.
Sendo assim, optou-se pelo uso da versão 2.6.0 que era a que possuía mais downloads no repositório do [Anaconda](https://anaconda.org/conda-forge/signxml/files) no momento dos testes.
Versões distintas da 3.2.0 e 2.6.0 não foram testadas. Para implementações de clientes em outras linguagens, favor verificar o valor da assinatura gerado pela respectiva biblioteca.

## Uso

A [classe](src/model/NotaOuroCliente.py) que representa o cliente retorna apenas a resposta HTTP às requisições.
O tratamento das respostas deve ser realizado na implementação do cliente pelos usuários.
Os exemplos de respostas podem ser encontrados no [*Swagger*](https://hom-nfoe.estaleiro.serpro.gov.br/API/swagger/index.html) da API. </br></br>
Exemplos de uso encontram-se na classe de [Testes](test/NotaOuroClienteExemplo.py).

## Clientes em outras linguagens

O cliente em Java pode ser encontrado em: </br>
[https://github.com/rscarvalho90/NF-e-Ouro-Java](https://github.com/rscarvalho90/NF-e-Ouro-Java)

O cliente em Node.js (TypeScript) pode ser encontrado em: </br>
[https://github.com/rscarvalho90/NF-e-Ouro-Node.js](https://github.com/rscarvalho90/NF-e-Ouro-Node.js)