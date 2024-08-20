#include "led_rgb.h"
#include <stdbool.h>
#include <driver/gpio.h>
#include <driver/ledc.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

ledc_info_t ledc_ch[LEDC_LED_CH_NUM];

void rgb_led_pwm_init(){
    int rgb_ch;
    // Definições de configuração para cada cor
    ledc_ch[0].channel = LEDC_CHANNEL_0;
    ledc_ch[0].gpio = LED_R_GPIO;
    ledc_ch[0].mode = LEDC_HIGH_SPEED_MODE;
    ledc_ch[0].timer_idx = LEDC_TIMER_0;

    ledc_ch[1].channel = LEDC_CHANNEL_1;
    ledc_ch[1].gpio = LED_G_GPIO;
    ledc_ch[1].mode = LEDC_HIGH_SPEED_MODE;
    ledc_ch[1].timer_idx = LEDC_TIMER_0;

    ledc_ch[2].channel = LEDC_CHANNEL_2;
    ledc_ch[2].gpio = LED_B_GPIO;
    ledc_ch[2].mode = LEDC_HIGH_SPEED_MODE;
    ledc_ch[2].timer_idx = LEDC_TIMER_0;

    // Configuração do temporizador LEDC
    ledc_timer_config_t ledc_timer = {
        .duty_resolution = LEDC_TIMER_8_BIT,
        .freq_hz = 1000,  // Frequência de 1000 Hz (pode ser ajustada para mudar a velocidade do efeito)
        .speed_mode = LEDC_HIGH_SPEED_MODE,
        .timer_num = LEDC_TIMER_0
    };
    ledc_timer_config(&ledc_timer);

    // Configuração dos canais LEDC
   for (rgb_ch = 0; rgb_ch < LEDC_LED_CH_NUM; rgb_ch++){
        ledc_channel_config_t ledc_channel = {
            .channel = ledc_ch[rgb_ch].channel,
            .duty = 0,
            .hpoint = 0,
            .gpio_num = ledc_ch[rgb_ch].gpio,
            .intr_type = LEDC_INTR_DISABLE,
            .speed_mode = ledc_ch[rgb_ch].mode,
            .timer_sel = ledc_ch[rgb_ch].timer_idx,
        };
        ledc_channel_config(&ledc_channel);
    }
}

void police_lights_task(void *pvParameter) {
    while (true) {
        // Vermelho
        ledc_set_duty(ledc_ch[0].mode, ledc_ch[0].channel, 255);
        ledc_set_duty(ledc_ch[1].mode, ledc_ch[1].channel, 0);
        ledc_set_duty(ledc_ch[2].mode, ledc_ch[2].channel, 0);
        ledc_update_duty(ledc_ch[0].mode, ledc_ch[0].channel);
        ledc_update_duty(ledc_ch[1].mode, ledc_ch[1].channel);
        ledc_update_duty(ledc_ch[2].mode, ledc_ch[2].channel);
        vTaskDelay(pdMS_TO_TICKS(300));

        // Espera 300ms no vermelho

        // Azul
        ledc_set_duty(ledc_ch[0].mode, ledc_ch[0].channel, 0);
        ledc_set_duty(ledc_ch[1].mode, ledc_ch[1].channel, 0);
        ledc_set_duty(ledc_ch[2].mode, ledc_ch[2].channel, 255);
        ledc_update_duty(ledc_ch[0].mode, ledc_ch[0].channel);
        ledc_update_duty(ledc_ch[1].mode, ledc_ch[1].channel);
        ledc_update_duty(ledc_ch[2].mode, ledc_ch[2].channel);
        vTaskDelay(pdMS_TO_TICKS(300));

        // Espera 300ms no azul

        // Branco
        ledc_set_duty(ledc_ch[0].mode, ledc_ch[0].channel, 255);
        ledc_set_duty(ledc_ch[1].mode, ledc_ch[1].channel, 255);
        ledc_set_duty(ledc_ch[2].mode, ledc_ch[2].channel, 255);
        ledc_update_duty(ledc_ch[0].mode, ledc_ch[0].channel);
        ledc_update_duty(ledc_ch[1].mode, ledc_ch[1].channel);
        ledc_update_duty(ledc_ch[2].mode, ledc_ch[2].channel);
        vTaskDelay(pdMS_TO_TICKS(300));

        // Espera 300ms no branco
    }
}

void christmas_lights_task(void *pvParameter) {
    while (true) {
        // Vermelho
        ledc_set_duty(ledc_ch[0].mode, ledc_ch[0].channel, 255);
        ledc_set_duty(ledc_ch[1].mode, ledc_ch[1].channel, 0);
        ledc_set_duty(ledc_ch[2].mode, ledc_ch[2].channel, 0);
        ledc_update_duty(ledc_ch[0].mode, ledc_ch[0].channel);
        ledc_update_duty(ledc_ch[1].mode, ledc_ch[1].channel);
        ledc_update_duty(ledc_ch[2].mode, ledc_ch[2].channel);
        vTaskDelay(pdMS_TO_TICKS(500)); // Espera 500ms no vermelho

        // Verde
        ledc_set_duty(ledc_ch[0].mode, ledc_ch[0].channel, 0);
        ledc_set_duty(ledc_ch[1].mode, ledc_ch[1].channel, 255);
        ledc_set_duty(ledc_ch[2].mode, ledc_ch[2].channel, 0);
        ledc_update_duty(ledc_ch[0].mode, ledc_ch[0].channel);
        ledc_update_duty(ledc_ch[1].mode, ledc_ch[1].channel);
        ledc_update_duty(ledc_ch[2].mode, ledc_ch[2].channel);
        vTaskDelay(pdMS_TO_TICKS(500)); // Espera 500ms no verde
    }
}

void alternating_lights_task(void *pvParameter) {
    bool isPoliceLights = true;

    while (true) {
        if (isPoliceLights) {
            police_lights_task(NULL); // Sequência de luzes da polícia
        } else {
            christmas_lights_task(NULL); // Sequência de luzes de Natal
        }

        // Alternância entre os efeitos
        isPoliceLights = !isPoliceLights;
        vTaskDelay(pdMS_TO_TICKS(5000));
    }
}

void update_rgb_led_intensity(int rpc_intensity_value) {
    int intensity = rpc_intensity_value;
    if (intensity < 0) {
        intensity = 0;
    } else if (intensity > 100) {
        intensity = 100;
    }
    int frequencia = intensity * 45 + 500;

    for (int i = 0; i < 3; i++) {
        ledc_set_freq(ledc_ch[i].mode, ledc_ch[i].channel, frequencia);
        ledc_set_duty(ledc_ch[i].mode, ledc_ch[i].channel, intensity);
        ledc_update_duty(ledc_ch[i].mode, ledc_ch[i].channel);
    }
}
