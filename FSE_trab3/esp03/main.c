/*
 * SPDX-FileCopyrightText: 2010-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include <stdio.h>
#include <inttypes.h>

#include "include/dht.h"
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "include/buzzer.h"
#include "include/dht.h"
#include <stdio.h>
#include "include/wifi.h"
#include "freertos/semphr.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "nvs_flash.h"
#include "include/mqtt.h"
#include "include/cJSON.h" 


SemaphoreHandle_t conexaoWifiSemaphore;
SemaphoreHandle_t conexaoMQTTSemaphore;
SemaphoreHandle_t envioMqttMutex;
QueueHandle_t interruption_queue;


void init_wifi(void * params)
{
  while(true)
  {
    if(xSemaphoreTake(conexaoWifiSemaphore, portMAX_DELAY))
    {
      mqtt_start();
    }
  }
}

void init_dht(){
    DHT11_init(04);
    xTaskCreate(&handle_dht, "Leitura DHT11", 4096, NULL, 1, NULL);
}

void init_buzzer(){
    buzzer_init();
}

void app_main(void)
{
    // Inicializa o NVS
    esp_err_t ret = nvs_flash_init();
    ESP_ERROR_CHECK(ret);
    
    conexaoWifiSemaphore = xSemaphoreCreateBinary();
    conexaoMQTTSemaphore = xSemaphoreCreateBinary();
    init_dht();
    init_buzzer();
    wifi_start();
    xTaskCreate(&init_wifi,  "Conexão ao MQTT", 4096, NULL, 1, NULL);
    xTaskCreate(&handle_dht, "Comunicação com Broker", 4096, NULL, 1, NULL);
    while (true)
    {
      vTaskDelay(1000 / portTICK_PERIOD_MS);
      printf("Verificando gpio\n");
      int status13 = gpio_get_level(13);
      int status23 = gpio_get_level(23);
      if (status13 == 1) {
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"buzzer\": true}");
        printf("Alerta de incendio\n");
        fire(10);
      }
      if (status23 == 1) {
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"buzzer\": true}");
        printf("Alerta de chamada\n");
        calling(4);
      }
      mqtt_envia_mensagem("v1/devices/me/attributes", "{\"buzzer\": false}");
    }


}