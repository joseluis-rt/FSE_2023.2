#ifndef FLAME_DETECTOR_H
#define FLAME_DETECTOR_H
#define FLAME_DETECTOR_DIGITAL_PIN 23

bool has_flame_detector_sensor();

void flame_detector_setup();

void flame_detector_posedge_handler();

bool get_flame_alarm_on();

void set_flame_alarm_on_to(bool value);

void flame_detector_turn_off_alarm();

void flame_detector_read_state_from_nvs();

#endif
