# ESP32 MQTT Thingsboard
Projeto final da disciplina Fundamentos de Sistemas Embarcados, semestre 2023.2,
da Universidade de Brasília, campus Gama.
Este projeto comunica-se por MQTT com um servidor Thingsboard, reportando como
atributo o sensor de fogo juntamente com o led da placa e o led rgb.

### Hardware
O projeto consiste em:

- Uma placa de desenvolvimento compatível com a DEVKIT V1, com um módulo : ESP-WROOM-32
- Um módulo LED RGB
- Um módulo de sensor de fogo

### Requisitos para compilação
O projeto depende de uma instalação válida dos seguintes softwares:

esp-idf v5.2

### Instruções de compilação

- Clone o projeto:
[git clone https://gitlab.com/wellpriz/Trabalho03FSE.git](https://github.com/FSE-2023-2/trabalho-final-2023-2-pedro_jose_pablo_ana.git)

- Entrar na pasta:

cd esp01
cd projeto_final

- Atualize os módulos:

git submodule update --init --recursive

- Configure o projeto:
  
idf.py menuconfig

- Compile os códigos-fonte:

idf.py build

- Grave o resultado na memória flash da ESP32:

idf.py flash

- Execute e monitore:

idf.py monitor

- Opções do Kconfig:
As seguintes opções podem ser configuradas usando-se o menuconfig:

Menu "Project's Wifi Configuration"

ESP_WIFI_SSID, o SSID da rede usada para se conectar à Internet

ESP_WIFI_PASSWORD, a senha da rede

ESP_MAXIMUM_RETRY, número máximo de tentativas de conexão
