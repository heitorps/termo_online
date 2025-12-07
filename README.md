# Termo Online

### Descrição
Versão de terminal multijogador competitivo do famoso jogo de navegador [termo](https://term.ooo/), projetada em python para a disciplina de Redes de Computadores do curso de Engenharia de Computação.
Confira o [relatório completo](https://drive.google.com/file/d/1HRkLNpAc1Dj9ls4MPeIQqZR24SI6Rn_6/view?usp=sharing) para mais informações.

### Tecnologias Utilizadas
Todo o programa foi feito em python, a conexão entre máquinas é proporcionada pela biblioteca "socket", que implementa uma conexão TCP de forma simples, permitindo configurar uma máquina como servidor e outra como cliente em uma rede local. Fez-se uso também de multithreading, a fim de evitar problemas de concorrência e possibilitar envio e recebimento de mensagens simultaneamente.

### Requisitos
A versão utilizada do python foi a 3.11
Recomendamos o uso de um ambiente virtual, no conda:
```sh
conda create --name my_machine python=3.11
conda activate my_machine
```
Nenhuma biblioteca adicional precisou ser instalada

### Instruções de Execução
O arquivo server.py refere-se ao servidor do jogo, para rodar:
```sh
python server.py
```
O servidor espera exatamente 2 instâncias de cliente antes de prosseguir sua execução
O arquivo client.py refere ao cliente do jogo, para rodar:
```sh
python client.py
```
O primeiro cliente a se conectar deve escolher a dificuldade do jogo e o modo de jogo antes de iniciar a partida
