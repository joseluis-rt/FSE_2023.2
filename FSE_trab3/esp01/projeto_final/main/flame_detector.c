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
#include "pthread.h"
#include "esp_pthread.h"

#include "flame_detector.h"
#include "mqtt.h"
#include "nvs_helper.h"
#include "led_rgb.h"

#define FLAME_DETECTOR_ALARM_LED_PIN 2

bool flame_alarm_on = false;
SemaphoreHandle_t flame_alarm_mutex;
extern SemaphoreHandle_t envioMqttMutex;

bool has_flame_detector_sensor(){
    return FLAME_DETECTOR_DIGITAL_PIN > 0;
}

bool get_flame_alarm_on(){
    bool ret = false;
    if (xSemaphoreTake(flame_alarm_mutex, portMAX_DELAY)){
        ret = flame_alarm_on;
        xSemaphoreGive(flame_alarm_mutex);
    }
    return ret;
}

void set_flame_alarm_on_to(bool value){
    if (xSemaphoreTake(flame_alarm_mutex, portMAX_DELAY)){
        flame_alarm_on = value;
        nvs_write_int_value("fire_alarm_on", value ? 1 : 0);
        xSemaphoreGive(flame_alarm_mutex);
    }
}

void flame_detector_setup(){
    if (!has_flame_detector_sensor())
        return;

    // DETECTOR DE CHAMA
    esp_rom_gpio_pad_select_gpio(FLAME_DETECTOR_DIGITAL_PIN);
    gpio_set_direction(FLAME_DETECTOR_DIGITAL_PIN, GPIO_MODE_INPUT);

    // Habilita pulldown
    gpio_pulldown_en(FLAME_DETECTOR_DIGITAL_PIN);
    // Desabilita pullup por segurança
    gpio_pullup_dis(FLAME_DETECTOR_DIGITAL_PIN);

    // Configura detecção de borda de subida
    gpio_set_intr_type(FLAME_DETECTOR_DIGITAL_PIN, GPIO_INTR_POSEDGE);

    // Configura led de alarme
    esp_rom_gpio_pad_select_gpio(FLAME_DETECTOR_ALARM_LED_PIN);
    gpio_set_direction(FLAME_DETECTOR_ALARM_LED_PIN, GPIO_MODE_OUTPUT);

    // Configura PWM do led de alarme
    ledc_timer_config_t timer_config = {
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .duty_resolution = LEDC_TIMER_8_BIT,
        .timer_num = LEDC_TIMER_0,
        .freq_hz = 1000,
        .clk_cfg = LEDC_AUTO_CLK};

    ledc_timer_config(&timer_config);

    ledc_channel_config_t channel_config = {
        .gpio_num = FLAME_DETECTOR_ALARM_LED_PIN,
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .channel = LEDC_CHANNEL_0,
        .timer_sel = LEDC_TIMER_0,
        .duty = 0,
        .hpoint = 0};

    ledc_channel_config(&channel_config);
    // Cria mutex para a região crítica da varíavel do alarme
    flame_alarm_mutex = xSemaphoreCreateMutex();
}

void *turn_on_led_alarm_till_is_off(void *args){
    ledc_fade_func_install(0);
    while (true){
        if (!get_flame_alarm_on()){
            ledc_fade_func_uninstall();
            gpio_set_level(FLAME_DETECTOR_ALARM_LED_PIN, 0);
            break;
        }
        ledc_set_fade_time_and_start(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 0, 1000, LEDC_FADE_WAIT_DONE);
        ledc_set_fade_time_and_start(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 255, 1000, LEDC_FADE_WAIT_DONE);
    }
    gpio_set_level(FLAME_DETECTOR_ALARM_LED_PIN, 0);
    //ledc_fade_func_uninstall();
    pthread_exit(NULL);
}

void flame_detector_turn_on_alarm(){
    if (!get_flame_alarm_on()){
        pthread_t tid;
        set_flame_alarm_on_to(true);
        pthread_create(&tid, 0, (void *(*)(void *))turn_on_led_alarm_till_is_off, (void *)NULL);
        pthread_detach(tid);
        // Inicialização do LED PWM
        rgb_led_pwm_init();

        // Criação da tarefa para alternância de luzes
        xTaskCreate(&alternating_lights_task, "alternating_lights_task", 2048, NULL, 5, NULL);
        bool ledLigado = true; // Começa com o LED aceso

        while (1) { // Loop infinito
            // Alterna entre ligado e desligado
            ledLigado = !ledLigado;

            // Envia o estado atual do LED para o ThingsBoard
            char mensagem[50]; // Tamanho da mensagem a ser enviada
            sprintf(mensagem, "{\"led_on\": %s}", ledLigado ? "true" : "false");
            mqtt_envia_mensagem("v1/devices/me/attributes", mensagem);

            sleep(1); // Atraso de 1 segundo (pode variar de acordo com o intervalo desejado)
        }

        if (xSemaphoreTake(envioMqttMutex, portMAX_DELAY)){
            mqtt_envia_mensagem("v1/devices/me/attributes", "{\"fire_alarm_on\": true}");
            //mqtt_envia_mensagem("v1/devices/me/attributes", "{\"led_on\": true}");
            xSemaphoreGive(envioMqttMutex);
        }
    }
    printf("Fogo ligado!\n");
}

void flame_detector_posedge_handler(){
    flame_detector_turn_on_alarm();
}

void flame_detector_turn_off_alarm(){
    if (get_flame_alarm_on() || gpio_get_level(FLAME_DETECTOR_ALARM_LED_PIN)){
        set_flame_alarm_on_to(false);
        ledc_fade_func_uninstall();
        gpio_set_level(FLAME_DETECTOR_ALARM_LED_PIN, 0);

        if (xSemaphoreTake(envioMqttMutex, portMAX_DELAY)){
            mqtt_envia_mensagem("v1/devices/me/attributes", "{\"fire_alarm_on\": false}");
            //mqtt_envia_mensagem("v1/devices/me/attributes", "{\"led_on\": false}");
            xSemaphoreGive(envioMqttMutex);
        }
         printf("Fogo desligado!\n");
    }
}

void flame_detector_read_state_from_nvs(){
    int value;

    if (nvs_read_int_value("fire_alarm_on", &value) && value == 1){
        flame_detector_turn_on_alarm();
    }
    else{
        flame_detector_turn_off_alarm();
    }
}
