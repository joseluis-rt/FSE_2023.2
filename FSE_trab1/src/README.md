# Estrutura dos Arquivos

O código é composto por vários arquivos, cada um desempenhando um papel específico no controle do cruzamento. Aqui está uma breve explicação da função de cada arquivo, organizados por ordem de importância no código.

1. **main.py**:
   - Este é o arquivo principal que inicia o programa.
   - Cria instâncias de dois cruzamentos e threads para controlá-los simultaneamente.
   - Gerencia a entrada do usuário para ativar modos noturnos ou de emergência.
   - Exibe informações sobre o fluxo de tráfego e infrações.

2. **cruzamento.py**:
   - Define a classe `cruzamento`, que representa um cruzamento.
   - Controla o estado dos semáforos, botões de pedestres, sensores e buzzer.
   - Implementa a lógica de controle do cruzamento.
     ### Função `controle_estados`
   - A função `controle_estados` é o coração do código de controle de cruzamento.
   - Ela gerencia os estados dos semáforos, monitora pedestres, detecta carros esperando e implementa a lógica de controle de tráfego.
   - O fluxo de controle do cruzamento é determinado por esta função, que é chamada repetidamente em loops para garantir a operação eficiente do cruzamento.

3. **sensor.py**:
   - Define a classe `sensor`, que representa um sensor de veículos.
   - Monitora o tráfego e calcula informações como velocidade média e infrações.
   - Detecta carros parados, excesso de velocidade e passagem com sinal vermelho.

4. **semaforo.py**:
   - Define a classe `semaforo` para controlar os semáforos.
   - Gerencia os LEDs do semáforo para exibir as cores corretas.
   - Oferece métodos para definir o semáforo como verde, amarelo, vermelho ou desligado.

5. **botao_pedestre.py**:
   - Define a classe `botao_pedestre` para monitorar os botões de pedestres.
   - Detecta quando um pedestre pressiona o botão para atravessar.
  
6. **buzzer.py**:
   - Define a classe `Buzzer` para controlar um buzzer.
   - Liga e desliga o buzzer para fornecer feedback sonoro no cruzamento.
  
7. **reset_gpio.py**:
   - `$ python3 reset_gpio.py`
   - Reinicia as GPIO da placa para configuração inicial.
