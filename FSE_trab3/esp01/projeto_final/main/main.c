#include <stdio.h>
#include <string.h>
#include "nvs_flash.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_http_client.h"
#include "freertos/semphr.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "wifi.h"
#include "mqtt.h"
#include "nvs_helper.h"
#include "flame_detector.h"
#include "led_rgb.h"
#include "botao.h"
#include "driver/rtc_io.h"
#include "esp32/rom/uart.h"
#include <esp_sleep.h>

#define INTERRUPTION_QUEUE_SIZE 15
#define MODO_BATERIA CONFIG_MODO_BATERIA

SemaphoreHandle_t conexaoWifiSemaphore;
SemaphoreHandle_t conexaoMQTTSemaphore;
SemaphoreHandle_t envioMqttMutex;
QueueHandle_t interruption_queue;

static void IRAM_ATTR gpio_isr_handler(void * args) {
  int pin = (int) args;
  
  xQueueSendFromISR(interruption_queue, &pin, NULL);
}

void handle_interruption(void * params) {
  int pin;

  while (true) {
    if (xQueueReceive(interruption_queue, &pin, portMAX_DELAY)) {
      if (pin == FLAME_DETECTOR_DIGITAL_PIN) {
        if (gpio_get_level(FLAME_DETECTOR_DIGITAL_PIN)) {
          flame_detector_posedge_handler();
          vTaskDelay(3000 / portTICK_PERIOD_MS);
          flame_detector_turn_off_alarm();
        }
      }
    }
  }
}

void mqtt_send_sleeping(int state){
  cJSON* response= cJSON_CreateObject();
  if (response == NULL){
      ESP_LOGE("LOW POWER", "Erro ao criar o json");
  }

  cJSON_AddItemToObject(response, "bateria", cJSON_CreateNumber(state));
  mqtt_envia_mensagem("v1/devices/me/attributes", cJSON_Print(response));
  vTaskDelay(1000 / portTICK_PERIOD_MS);
}

void handle_low_power() {
    // Espere algum tempo antes de entrar em modo de baixo consumo
    vTaskDelay(pdMS_TO_TICKS(10000)); // Por exemplo, 10 segundos

    mqtt_send_sleeping(1);

    ESP_LOGI("SYS", "SLEEPING");
    uart_tx_wait_idle(CONFIG_ESP_CONSOLE_UART_NUM);
    esp_deep_sleep_start();
    esp_restart();
}

void conectado_wifi(void * params){
    while(true) {
        if(xSemaphoreTake(conexaoWifiSemaphore, portMAX_DELAY)){
            ESP_LOGI("[Network]", "Conexao wi-fi estabelecida");
            // Processamento Internet
            mqtt_start();
            ESP_LOGI("[Mqtt_broker]", "Comunicação com o broker: mqtt://164.41.98.25 iniciada");
            
            // Verificações para ação com base na conexão MQTT
            while (true) {
                if (xSemaphoreTake(conexaoMQTTSemaphore, portMAX_DELAY)) {
                    if (MODO_BATERIA == 0) {
                        mqtt_send_sleeping(0);
                        flame_detector_setup();
                    } else if (MODO_BATERIA == 1) {
                        handle_low_power();
                    }
                }
                vTaskDelay(pdMS_TO_TICKS(500)); // Ajuste o atraso conforme necessário
            }
        }
    }
}

void app_main(void) {
  // Inicializa o NVS
  setup_nvs();
  
  conexaoWifiSemaphore = xSemaphoreCreateBinary();
  conexaoMQTTSemaphore = xSemaphoreCreateBinary();
  envioMqttMutex = xSemaphoreCreateMutex();

  wifi_start();
  flame_detector_setup();

  interruption_queue = xQueueCreate(INTERRUPTION_QUEUE_SIZE, sizeof(int));
  xTaskCreate(&handle_interruption,  "Trata interrupções", 2048, NULL, 1, NULL);

  gpio_install_isr_service(0);
  gpio_isr_handler_add(FLAME_DETECTOR_DIGITAL_PIN, gpio_isr_handler, (void *) FLAME_DETECTOR_DIGITAL_PIN);

  xTaskCreate(&conectado_wifi,  "Conexão ao MQTT", 4096, NULL, 1, NULL);
  vTaskDelay(1000 / portTICK_PERIOD_MS);
  flame_detector_read_state_from_nvs();
}