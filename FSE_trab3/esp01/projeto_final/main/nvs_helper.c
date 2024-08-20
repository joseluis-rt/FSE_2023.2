#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "esp_log.h"
#include "esp_event.h"
#include "freertos/semphr.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "sdkconfig.h"
#include "driver/adc.h"
#include "driver/ledc.h"
#include "esp_system.h"
#include "nvs.h"
#include "nvs_flash.h"

#include "nvs_helper.h"

#define ATTRS_STATE_NAMESPACE "attrs"

void setup_nvs() {
    esp_err_t ret = nvs_flash_init();

    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}

bool nvs_read_int_value(const char * key, int * value) {
    nvs_handle attrs_state_handler;
    esp_err_t ret = nvs_open(ATTRS_STATE_NAMESPACE, NVS_READONLY, &attrs_state_handler);

    if (ret != ESP_OK) return false;

    int32_t read_value = 0;
    ret = nvs_get_i32(attrs_state_handler, key, &read_value);

    if (ret == ESP_OK) {
        *value = (int) read_value;
        return true;
    }

    ESP_LOGE("NVS", "Falha ao acessar o NVS: (%s)", esp_err_to_name(ret));
    nvs_close(attrs_state_handler);

    return false;
}

bool nvs_write_int_value(const char * key, int value) {
    nvs_handle attrs_state_handler;
    esp_err_t ret = nvs_open(ATTRS_STATE_NAMESPACE, NVS_READWRITE, &attrs_state_handler);

    if (ret != ESP_OK) return false;

    ret = nvs_set_i32(attrs_state_handler, key, value);

    if (ret == ESP_OK)
        return true;

    ESP_LOGE("NVS", "Falha ao acessar o NVS: (%s)", esp_err_to_name(ret));

    nvs_commit(attrs_state_handler);
    nvs_close(attrs_state_handler);

    return false;
}
