#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "esp_system.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/queue.h"
#include "lwip/sockets.h"
#include "lwip/dns.h"
#include "lwip/netdb.h"
#include "cJSON.h"
#include "esp_log.h"
#include "mqtt_client.h"
#include "mqtt.h"
#include "led_rgb.h"

#define TAG "MQTT"
#define MAX_RECONNECTION_ATTEMPTS 5
#define RECONNECTION_INTERVAL_MS 2000

extern SemaphoreHandle_t conexaoMQTTSemaphore;
esp_mqtt_client_handle_t client;

uint16_t request_id = 0;

int reconnection_attempt = 0;
bool mqtt_connected = false;
void ajustarFrequenciaLED(int led_power) {
    if (led_power > 0 && led_power <= 255) {
        int frequencia = led_power * 10;
        update_rgb_led_intensity(led_power);
        printf("Ajustando a frequência do LED RGB para: %d Hz\n", frequencia);
    } else {
        printf("Valor de led_power fora do intervalo válido.\n");
    }
}

void handle_mqtt_request(char* message, uint16_t request_id) {
    cJSON *root = cJSON_Parse(message);
    if (root == NULL) {
        cJSON_Delete(root);
        return;
    }

    cJSON *method = cJSON_GetObjectItemCaseSensitive(root, "method");
    cJSON *params = cJSON_GetObjectItemCaseSensitive(root, "params");

    if (cJSON_IsString(method) && cJSON_IsObject(params)) {
        if (strcmp(method->valuestring, "led_power") == 0) {
            cJSON *power_value = cJSON_GetObjectItemCaseSensitive(params, "power_value");

            if (cJSON_IsNumber(power_value)) {
                int led_power = power_value->valueint;
                ajustarFrequenciaLED(led_power);

                char response_topic[50];
                sprintf(response_topic, "v1/devices/me/rpc/response/%d", request_id);
                esp_mqtt_client_publish(client, response_topic, "{\"led_power\": %d}", led_power, 0, 0);

                // Envio do atributo para a dashboard
                cJSON *attribute = cJSON_CreateObject();
                cJSON_AddItemToObject(attribute, "led_power", cJSON_CreateNumber(led_power));
                mqtt_envia_mensagem("v1/devices/me/rpc/request/+", cJSON_PrintUnformatted(attribute));
                cJSON_Delete(attribute);
            }
        }
    }
    cJSON_Delete(root);
}

void reconnect_mqtt() {
    while (!mqtt_connected && reconnection_attempt < MAX_RECONNECTION_ATTEMPTS) {
        esp_mqtt_client_reconnect(client);
        vTaskDelay(RECONNECTION_INTERVAL_MS / portTICK_PERIOD_MS);
        reconnection_attempt++;
    }
}

static esp_err_t mqtt_event_handler_cb(esp_mqtt_event_handle_t event){
    esp_mqtt_client_handle_t client = event->client;
    int msg_id;
    
    switch (event->event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");
            xSemaphoreGive(conexaoMQTTSemaphore);
            msg_id = esp_mqtt_client_subscribe(client, "v1/devices/me/rpc/request/+", 0);
            break;
        case MQTT_EVENT_DISCONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_DISCONNECTED");
            break;
        case MQTT_EVENT_SUBSCRIBED:
            ESP_LOGI(TAG, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_UNSUBSCRIBED:
            ESP_LOGI(TAG, "MQTT_EVENT_UNSUBSCRIBED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_PUBLISHED:
            ESP_LOGI(TAG, "MQTT_EVENT_PUBLISHED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_DATA:
            ESP_LOGI(TAG, "MQTT_EVENT_DATA");
            printf("TOPIC=%.*s\r\n", event->topic_len, event->topic);
            printf("DATA=%.*s\r\n", event->data_len, event->data);
            const char *data = event->data;
            handle_mqtt_request(data, request_id);
            break;
        case MQTT_EVENT_ERROR:
            ESP_LOGI(TAG, "MQTT_EVENT_ERROR");
            reconnect_mqtt();
            break;
        default:
            ESP_LOGI(TAG, "Other event id:%d", event->event_id);
            break;
    }
    return ESP_OK;
}

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    ESP_LOGD(TAG, "Event dispatched from event loop base=%s, event_id=%d", base, event_id);
    mqtt_event_handler_cb(event_data);
    // Handle MQTT request data
    esp_mqtt_event_handle_t event = event_data;
    if (event_id == MQTT_EVENT_DATA) {
        if (strncmp(event->topic, "v1/devices/me/rpc/request/", strlen("v1/devices/me/rpc/request/")) == 0) {
            const char *data = event->data;
            handle_mqtt_request(data, request_id);
        }
    }
}

void mqtt_start(){
    esp_mqtt_client_config_t mqtt_config = {
        .broker.address.uri = "mqtt://164.41.98.25",
        .credentials.username = "IUictnb0BbYmPL3GWDdN" // Token do Dispositivo
    };
    client = esp_mqtt_client_init(&mqtt_config);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
    esp_mqtt_client_start(client);
}

void mqtt_envia_mensagem(char * topico, char * mensagem){
    int message_id = esp_mqtt_client_publish(client, topico, mensagem, 0, 1, 0);
    ESP_LOGI(TAG, "Mensagem enviada, ID: %d", message_id);
}