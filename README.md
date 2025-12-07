A versão utilizada do python foi a 3.11
Recomendamos o uso de um ambiente virtual, no conda:
```sh
conda create --name my_machine python=3.11
conda activate my_machine
```
O arquivo server.py refere-se ao servidor do jogo, para rodar basta:
```sh
python server.py
```
O programa vai esperar até que duas conexões sejam realizadas antes de prosseguir sua execução
O arquivo client.py refere ao cliente do jogo, o servidor esperar exatamente 2 instâncias de cliente, para rodar basta:
```sh
python client.py
```
O primeiro cliente a se conectar é obrigado a escolher a dificuldade do jogo e o modo de jogo antes do início efetivo deste
