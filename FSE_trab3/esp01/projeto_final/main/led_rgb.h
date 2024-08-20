#ifndef LED_H_
#define LED_H_

#include <stdint.h>

#define LED_R_GPIO      5
#define LED_B_GPIO      4
#define LED_G_GPIO      17
#define LEDC_LED_CH_NUM  3
#define LEDC_TIMER_BIT_NUM  8
#define LEDC_BASE_FREQ      5000

typedef struct{
    int channel;
    int gpio;
    int mode;
    int timer_idx;
} ledc_info_t;

void rgb_led_pwm_init();
void rgb_set_color(uint8_t red, uint8_t green, uint8_t blue);
void christmas_lights_task(void *pvParameter);
void police_lights_task(void *pvParameter);
void alternating_lights_task(void *pvParameter);
void update_rgb_led_intensity(int intensity);

#endif /* LED_H_ */