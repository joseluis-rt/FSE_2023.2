- **Aluno:** José Luís Ramos Teixeira
- **Matrícula:** 19/0057858
# Trabalho 1 (2023-2)

Este é o [Trabalho 1](https://gitlab.com/fse_fga/trabalhos-2023_2/trabalho-1-2023-2) da disciplina de Fundamentos de Sistemas Embarcados (FSE) da [UnB Gama - FGA](https://fga.unb.br/). 
- A pasta principal do trabalho é o `src` e é a única necessária para rodar o programa;
- A pasta `interface` é apenas uma versão inicial de como estava ficando minha Interface Gráfica, porém não foi finalizada;


<a name="top0"></a>
## Sumário
1. [Dependências](#top1)
2. [Executando](#top2)
3. [Funcionamento](#top3)
4. [Objetivos do Trabalho](#top4)
5. [GPIOs Utilizadas](#top5)
6. [Pontos de Melhoria](#top6)
7. [Apresentação em Vídeo](#top7)


<br/>

<img align="center" alt="Raspverry Pi" height="40" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/raspberrypi/raspberrypi-original.svg"><img align="center" alt="Python" height="40" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">


<a name="top1"></a>
## 1. Dependências
* python3 (versão utilizada: 3.11.6)

* [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)


  Para instalar:
  ```bash
  $ pip3 install RPi.GPIO
  ```

  A documentação da RPi.GPIO se encontra em
https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/

[(Sumário - voltar ao topo)](#top0)
<br/>


<a name="top2"></a>
## 2. Executando
Para executar, clone o repositório e transfira a pasta `src` para uma das Raspberry.
 
Na raiz do projeto execute o seguinte comando:

```bash
$ python3 src/main.py
```
- Para ativar o modo NOTURNO digite a qualquer momento a tecla `N | n`;
- Para ativar o modo EMERGENCIA digite a qualquer momento a tecla `E | e`;
- Para desativar o modo NOTURNO ou EMERGENCIA digite a qualquer momento a tecla `X | x`;
- Interaja com o board (da Raspberry conectada) para visualizar as informações de cada cruzamento no terminal serem atualizadas;
- Para finalizar o programa digite as teclas `CTRL+C`.

[(Sumário - voltar ao topo)](#top0)
<br/>


<a name="top3"></a>
## 3. Funcionamento

O programa controla o funcionamento do cruzamento, alternando os semáforos, monitorando sensores de tráfego e respondendo aos botões de pedestres. Ele também registra infrações, como excesso de velocidade e passagem com o sinal vermelho.

O usuário pode interagir com o programa para ativar modos noturnos ou de emergência. O programa exibe informações detalhadas sobre o fluxo de tráfego e infrações, facilitando a monitoração do cruzamento.

![Board Terminal](/FSE_trab1/assets/board_terminal.png)

[Explore o README do src](https://github.com/joseluis-rt/FSE_2023.2/tree/main/FSE_trab1/src) para obter mais informações sobre os arquivos utilizados neste projeto `main.py, cruzamento.py, sensor.py, ...`.

[(Sumário - voltar ao topo)](#top0)
<br/>


<a name="top4"></a>
## 4. Objetivos do Trabalho

Este trabalho tem por objetivo a criação de um sistema distribuído para o controle e monitoramento de um grupo de cruzamentos de sinais de trânsito. O sistema deve ser desenvolvido para funcionar em um conjunto de placas Raspberry Pi para o controle local e monitoramento dos sinais do cruzamento junto aos respectivos sensores que monitoram as vias. Dentre os dispositivos envolvidos estão: 

- Controle de temporização e acionamento dos sinais de trânsito;
- Acionamento de botões de passagens de pedestres;
- Monitoramento de sensores de passagem de carros;
- Monitoramento de velocidade da via e o avanço de sinal vermelho.

A imagem a seguir ilustra um **cruzamento de trânsito**:

<img align="center" alt="Cruzamento de Transito" height="250" width="280" src="https://img.freepik.com/free-vector/colored-isolated-city-isometric-composition-with-road-crosswalk-city-center-vector-illustration_1284-30528.jpg">

Cada cruzamento possui:
- 4 Sinais de Trânsito (Em pares);
- 2 botões de acionamento para pedestres (pedir passagem), uma para cada direção;
- 2 Sensores de velocidade/presença/passagem de carros (nas vias auxiliares, um em cada direção);
- 2 Sensores de velocidade/presença/passagem de carros (nas vias principais, um em cada direção);
- 1 Sinalização de áudio (buzzer) para sinalizar quando o sinal está mudando de estado (quando o cruzamento de pedestres irá ser fechado);

Composto por:
- 01 Placa Raspberry Pi 3/4;
- 04 Saídas GPIO (LEDs) representando os semáforos;
- 02 Entradas sendo os botões de pedestre;
- 02 Entradas sendo os sensores de velocidade/presença/contagem de veículos das vias auxiliares (2 por cruzamento);
- 02 Entradas sendo os sensores de velocidade/presença/contagem (4 por cruzamento);
- Saída de áudio para efeito sonoro estado do sinal para deficientes auditivos;

[(Sumário - voltar ao topo)](#top0)
<br/>


<a name="top5"></a>
## 5. GPIOs Utilizadas

Na figura abaixo apresento a arquitetura geral do sistema, destacando as GPIOs utilizadas em cada cruzamento:

<br/>

![Figura](/FSE_trab1/assets/cruzamentos_gpio.png)

<br/>

[(Sumário - voltar ao topo)](#top0)
<br/>

<a name="top6"></a>
## 6. Pontos de Melhoria

1. **Implementação do TCP/IP**: Ainda é necessário implementar a comunicação TCP/IP para conectar o servidor central aos dispositivos distribuídos. Para conectar os cruzamentos de forma individual mais eficientemente.

2. **Interface Gráfica**: Inicialmente, comecei a criar uma interface gráfica com a biblioteca Tkinter:
    ```bash
    $ sudo apt-get install python3-tk
    ```
    Porém interrompi sua implementação devido à falta de suporte nas placas utilizadas. O progresso ainda pode ser visualizado na pasta `interface`.
    
    - Caso queira testar, dentro da pasta `interface` digite o comando:
      ```bash
      $ python3 main.py
      ```
    - A interface gráfica ficou assim:
  
      <img align="center" alt="Interface Gráfica" height="500" width="500" src="/FSE_trab1/assets/interface_grafica.png">


[(Sumário - voltar ao topo)](#top0)
<br/>

<a name="top7"></a>
## 7. Apresentação em Vídeo

**Para assistir ao vídeo, clique na imagem abaixo:**

[![Assista ao vídeo](https://img.youtube.com/vi/link da imagem do video)](colocar video)

Também é possível acessar o vídeo diretamente pelo link: [Vídeo no YouTube](colocar video)

[(Sumário - voltar ao topo)](#top0)
<br/>

