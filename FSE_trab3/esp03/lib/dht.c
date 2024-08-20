/*
 * MIT License
 * 
 * Copyright (c) 2018 Michele Biondi
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
*/

#include "esp_timer.h"
#include "driver/gpio.h"
#include "rom/ets_sys.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "../include/dht.h"
#include "../include/cJSON.h"
#include "../include/mqtt.h"

static gpio_num_t dht_gpio;
static int64_t last_read_time = -2000000;
static struct dht11_reading last_read;

static int _waitOrTimeout(uint16_t microSeconds, int level) {
    int micros_ticks = 0;
    while(gpio_get_level(dht_gpio) == level) { 
        if(micros_ticks++ > microSeconds) 
            return DHT11_TIMEOUT_ERROR;
        ets_delay_us(1);
    }
    return micros_ticks;
}

static int _checkCRC(uint8_t data[]) {
    if(data[4] == (data[0] + data[1] + data[2] + data[3]))
        return DHT11_OK;
    else
        return DHT11_CRC_ERROR;
}

static void _sendStartSignal() {
    gpio_set_direction(dht_gpio, GPIO_MODE_OUTPUT);
    gpio_set_level(dht_gpio, 0);
    ets_delay_us(20 * 1000);
    gpio_set_level(dht_gpio, 1);
    ets_delay_us(40);
    gpio_set_direction(dht_gpio, GPIO_MODE_INPUT);
}

static int _checkResponse() {
    /* Wait for next step ~80us*/
    if(_waitOrTimeout(80, 0) == DHT11_TIMEOUT_ERROR)
        return DHT11_TIMEOUT_ERROR;

    /* Wait for next step ~80us*/
    if(_waitOrTimeout(80, 1) == DHT11_TIMEOUT_ERROR) 
        return DHT11_TIMEOUT_ERROR;

    return DHT11_OK;
}

static struct dht11_reading _timeoutError() {
    struct dht11_reading timeoutError = {DHT11_TIMEOUT_ERROR, -1, -1};
    return timeoutError;
}

static struct dht11_reading _crcError() {
    struct dht11_reading crcError = {DHT11_CRC_ERROR, -1, -1};
    return crcError;
}

void DHT11_init(gpio_num_t gpio_num) {
    /* Wait 1 seconds to make the device pass its initial unstable status */
    vTaskDelay(1000 / portTICK_PERIOD_MS);
    dht_gpio = gpio_num;
}

struct dht11_reading DHT11_read() {
    /* Tried to sense too son since last read (dht11 needs ~2 seconds to make a new read) */
    if(esp_timer_get_time() - 2000000 < last_read_time) {
        return last_read;
    }

    last_read_time = esp_timer_get_time();

    uint8_t data[5] = {0,0,0,0,0};

    _sendStartSignal();

    if(_checkResponse() == DHT11_TIMEOUT_ERROR)
        return last_read = _timeoutError();
    
    /* Read response */
    for(int i = 0; i < 40; i++) {
        /* Initial data */
        if(_waitOrTimeout(50, 0) == DHT11_TIMEOUT_ERROR)
            return last_read = _timeoutError();
                
        if(_waitOrTimeout(70, 1) > 28) {
            /* Bit received was a 1 */
            data[i/8] |= (1 << (7-(i%8)));
        }
    }

    if(_checkCRC(data) != DHT11_CRC_ERROR) {
        last_read.status = DHT11_OK;
        last_read.temperature = data[2];
        last_read.humidity = data[0];
        return last_read;
    } else {
        return last_read = _crcError();
    }
}

struct DHT11Data useDHT11() {
    gpio_num_t sensorPin = 04;
    DHT11_init(sensorPin);

    struct dht11_reading reading = DHT11_read();
    struct DHT11Data data;

    if (reading.status == DHT11_OK) {
        data.temperature = reading.temperature;
        data.humidity = reading.humidity;
    } else {
        data.temperature = -1;
        data.humidity = -1;
    }

    return data;
}

void handle_dht(void * params){

    while(true)
    {
    struct dht11_reading dht11_data_tic;
    struct dht11_reading dht11_data_tac;
    struct dht11_reading dht11_data_tec;
    struct dht11_reading dht11_data;

    
    do {
        dht11_data_tic = DHT11_read();
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        dht11_data_tac = DHT11_read();
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        dht11_data_tec = DHT11_read();
    } while (
        (
            dht11_data_tic.temperature > dht11_data_tac.temperature + 3 &&
            dht11_data_tic.temperature > dht11_data_tec.temperature + 3 &&
            dht11_data_tac.temperature > dht11_data_tec.temperature + 3
            )||(
            dht11_data_tic.temperature < dht11_data_tac.temperature - 3 &&
            dht11_data_tic.temperature < dht11_data_tec.temperature - 3 &&
            dht11_data_tac.temperature < dht11_data_tec.temperature - 3
            )
        );

    dht11_data.temperature = (
        dht11_data_tic.temperature +
        dht11_data_tac.temperature + 
        dht11_data_tec.temperature
        )/3;

    dht11_data.humidity = (
        dht11_data_tic.humidity +
        dht11_data_tac.humidity +
        dht11_data_tec.humidity
        )/3;

    if (
        dht11_data_tic.status == DHT11_OK &&
        dht11_data_tac.status == DHT11_OK &&
        dht11_data_tec.status == DHT11_OK
        ){
        cJSON* response= cJSON_CreateObject();
        cJSON_AddItemToObject(response, "temperatura", cJSON_CreateNumber(dht11_data.temperature));
        cJSON_AddItemToObject(response, "umidade", cJSON_CreateNumber(dht11_data.humidity));
        mqtt_envia_mensagem("v1/devices/me/telemetry", cJSON_Print(response));
    };

    if (dht11_data.temperature > 28) {
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_alta\": true}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_normal\": false}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_baixa\": false}");
    }else if (dht11_data.temperature < 18) {
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_alta\": false}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_normal\": false}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_baixa\": true}");
    }else {
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_alta\": false}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_normal\": true}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"temperatura_baixa\": false}");
    };

    if (dht11_data.humidity > 70) {
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_alta\": true}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_normal\": false}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_baixa\": false}");

    }else if (dht11_data.humidity < 40) {
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_alta\": false}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_normal\": false}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_baixa\": true}");
    }else {
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_alta\": false}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_normal\": true}");
        mqtt_envia_mensagem("v1/devices/me/attributes", "{\"umidade_baixa\": false}");
    };
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    };
}
