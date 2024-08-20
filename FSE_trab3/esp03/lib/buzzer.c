#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_log.h"
#include "driver/gpio.h"

#define buzzer 15

void buzzer_on()
{
    gpio_set_level(buzzer, 1);
}

void buzzer_off()
{
    gpio_set_level(buzzer, 0);
}

void fast_delay()
{
    vTaskDelay(100 / portTICK_PERIOD_MS);
}

void middle_delay()
{
    vTaskDelay(1000 / portTICK_PERIOD_MS);
}

void buzzer_init()
{
    esp_rom_gpio_pad_select_gpio(buzzer);
    gpio_set_direction(buzzer, GPIO_MODE_OUTPUT);
    buzzer_off();
}

void fire(int time)
{
    printf("Alerta de Incêndio!\n");
    esp_rom_gpio_pad_select_gpio(buzzer);
    gpio_set_direction(buzzer, GPIO_MODE_OUTPUT);
    for (int i = 0; i < time; i++) {
        buzzer_on();
        fast_delay();
        buzzer_off();
        fast_delay();
    }
}

void calling(int time)
{
    esp_rom_gpio_pad_select_gpio(buzzer);
    gpio_set_direction(buzzer, GPIO_MODE_OUTPUT);
    for (int i = 0; i < time; i++) {
        for (int j = 0; j < 3; j++) {
            buzzer_on();
            fast_delay();
            buzzer_off();
            fast_delay();
        }
        buzzer_on();
        middle_delay();
    }
    
    buzzer_off();
}

