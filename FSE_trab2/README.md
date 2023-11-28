- **Aluno...........** José Luís Ramos Teixeira
- **Matrícula.....** 19/0057858
- **Data..............** 24/11/2023
# Trabalho 2 (2023-2)

Este é o [Trabalho 2](https://gitlab.com/fse_fga/trabalhos-2023_2/trabalho-2-2023-2) da disciplina de Fundamentos de Sistemas Embarcados (FSE) da [UnB Gama - FGA](https://fga.unb.br/). 

<a name="top0"></a>
## Sumário
1. [Instruções](#top1)
2. [Implementação do controlador PID](#top2)
3. [Leitura da Temperatura Ambiente](#top3)
4. [Comunicação UART](#top4)
5. [Mostrador no LCD](#top5)
6. [Apresentação em Vídeo](#top6)


<br/>

<img align="center" alt="Raspverry Pi" height="40" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/raspberrypi/raspberrypi-original.svg"><img align="center" alt="Python" height="40" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">


<a name="top1"></a>
## 1. Instruções
### Dependências
Python3 - (3.11.6) | Pip - (20.2.3) | Pyserial - (3.5) | Bmp280 - (0.0.4) | i2cdevice - (1.0.0) | RPi.GPIO - (0.7.1 | Smbus - (1.1.post2)


  Para instalar:
  ```bash
  $ pip install pyserial
  $ pip install bmp280
  $ pip install RPi.GPIO
  $ pip install smbus
  ```

### Executando
Para executar, clone o repositório e transfira a pasta `src` para uma das Raspberry.
 
Na raiz do projeto execute o seguinte comando:

```bash
$ python3 src/main.py
```
<br/>

```
1. Inicialmente, o programa realizará a descida do elevador até alcançar o valor '0' no encoder;
2. Em seguida, ele iniciará a ascensão, verificando os valores do encoder correspondentes a cada andar (Térreo, 1º, 2º, 3º);
3. Após essa verificação, o programa executará a lógica necessária para direcionar o elevador aos andares desejados, de acordo com os botões selecionados na board;
4. Durante todo o processo, a atualização no visor LCD será realizada, exibindo informações como o andar atual, o estado do elevador e a temperatura ambiente.
```

<br/>

[(Sumário - voltar ao topo)](#top0)
<br/>




<a name="top2"></a>
## 2. Implementação do controlador PID
- A implementação do controlador PID visa proporcionar um controle preciso e eficiente do elevador, permitindo que ele se mova de forma suave e precisa entre diferentes andares. 
- Vamos entender o funcionamento e a integração dessa implementação nos diferentes arquivos do projeto.

### 2.1. Entendendo a Implementação do PID:

#### main.py:
```
- Inicia configurando o logger e importando os módulos, incluindo o `pid`.
- Define as constantes do `controlador PID`, como o ganho proporcional (Kp), o ganho integral (Ki) e o ganho derivativo (Kd).
- Inicializa o objeto `PID` (`pid_control`) e configura suas constantes.
- Durante a execução do elevador, o PID é utilizado para controlar a movimentação, ajustando a potência do motor com base nos valores do encoder.
```

#### gpio.py:
```
- A classe `GPIOController` inicializa o PID e controla o motor do elevador com base nos valores do encoder.
- Ao mover o elevador para diferentes andares, o PID é utilizado para ajustar a potência do motor de acordo com a referência do andar desejado.
```

#### pid.py:
```
- O módulo `pid` contém a classe `PID`, responsável por implementar o controlador PID.
- O método `controle` é fundamental, calculando o sinal de controle com base nos erros proporcional, integral e derivativo.
- Os ganhos (Kp, Ki, Kd) e a referência são ajustados dinamicamente durante a execução.
```

### 2.2. Exemplo de Funcionamento:
```
- No main.py, o elevador desce até o terreo (andar 0) e, em seguida, reconhece os andares (Reconhecendo andares...).
- Em seguida, move-se para o andar desejado, utilizando o PID para controlar a movimentação.
- O PID ajusta dinamicamente os ganhos e a referência para garantir um movimento preciso e controlado.
```


[(Sumário - voltar ao topo)](#top0)
<br/>
<a name="top3"></a>
## 3. Leitura da Temperatura Ambiente
A obtenção da temperatura ambiente é crucial para monitorar as condições internas do elevador. Dependendo da placa utilizada, o código pode empregar os módulos i2c_bme280.py ou i2c_bmp280.py. Abaixo estão as implementações correspondentes:

Utilizando **`i2c_bme280.py`**:
```bash
import smbus2
import bme280 
from time import sleep

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)

def temp_ambiente():
    bme280_data = bme280.sample(bus, address)
    temp_ambiente = bme280_data.temperature
    return temp_ambiente

```

Utilizando **`i2c_bmp280.py`**:
```bash
import smbus2
from bmp280 import BMP280 
from time import sleep

# Cria uma instância da classe BMP280
bmp280 = BMP280()

def temp_ambiente():
    temperature = bmp280.get_temperature()
    return temperature
```

De acordo com a utilizada pela placa, no arquivo **`cmds.py`** irei pegar a temperatura a partir da def **`temp_ambiente`**

Arquivo **`cmds.py`**:
```bash
...
import i2c_bmp280
# import i2c_bme280

temperature = i2c_bmp280.temp_ambiente()
rounded_temperature = round(temperature, 2)

...
#formato para envio da temp no protocolo UART Modbus
le_temp = [cod[0], 0x16, 0xD1, *struct.pack('<f', temperature), *id]
...

def apurar_temp():
    valor_temp = uart.envia_recebe(le_temp)
    return valor_temp
...
```

[(Sumário - voltar ao topo)](#top0)
<br/>
<a name="top4"></a>
## 4. Comunicação UART
O módulo UART é fundamental para a comunicação Modbus no projeto, utilizando a validação do CRC. Abaixo estão os trechos de código mais relevantes:

Arquivo **`uart.py`**:
```bash
import logging
import serial
import struct
import crc

uart0_filestream = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

# Verifica se a UART foi inicializada com sucesso
if uart0_filestream == -1:
    logging.error("Não foi possível iniciar a UART.\n")
else:
    logging.info("UART inicializada!\n")

def envia_comando(comando, *args):
    # (código para empacotar o comando e calcular o CRC)

    uart0_filestream.write(mensagem_crc)

def recebe_resposta():
    # (código para receber a resposta e verificar o CRC)

def envia_recebe(comando, *args):
    # (código para enviar o comando, aguardar e receber a resposta)

```

Arquivo **`cmds.py`**:
```bash
import ...
... 

# formatação dos tipos de *args para uart.py
le_encoder = [cod[0], 0x23, 0xC1, *id]
le_pwm = [cod[0], 0x16, 0xC2, *struct.pack("<i", pwm_global), *id] 
le_temp = [cod[0], 0x16, 0xD1, *struct.pack('<f', temperature), *id]
le_btnT = [cod[0], 0x03, 0x00, 1, *id]
...

# defs para uart.py
def apurar_encoder():
    valor_encoder = uart.envia_recebe(le_encoder)
    return valor_encoder

def apurar_pwm():
    valor_pwm = uart.envia_recebe(le_pwm)
    return valor_pwm

def apurar_temp():
    valor_temp = uart.envia_recebe(le_temp)
    return valor_temp

...
```

E finalmente podemos chamar na main ou nos outros arquivos a forma correta de envio de mensagens **UART Modbus**.

[(Sumário - voltar ao topo)](#top0)
<br/>
<a name="top5"></a>
## 5. Mostrador no LCD
No arquivo **`cmds.py`**, a função apurar_lcd() utiliza as funções do arquivo **`lcd.py`** para exibir informações relevantes no LCD, como o andar atual e a temperatura ambiente.

```bash
import lcd
...

def apurar_lcd():
    lcd.lcd_init()
    
    while True:
        lcd.lcdLoc(lcd.LINE1)
        lcd.typeln(f"{controle.andar_atual} {controle.status}")
        lcd.lcdLoc(lcd.LINE2)
        lcd.typeln(f"Temp: {rounded_temperature} C")
        time.sleep(2)
```

Esta função é chamada no arquivo **`main.py`** para exibir informações na inicialização do programa.



[(Sumário - voltar ao topo)](#top0)
<br/>
<a name="top6"></a>
## 6. Apresentação em Vídeo

**Para assistir ao vídeo, clique na imagem abaixo:**

[![Assista ao vídeo](https://img.youtube.com/vi/-4hHBN4TRqU/maxresdefault.jpg)](https://www.youtube.com/watch?v=-4hHBN4TRqU)

Também é possível acessar o vídeo diretamente pelo link: [Vídeo no YouTube](https://youtu.be/-4hHBN4TRqU)

[(Sumário - voltar ao topo)](#top0)
<br/>
