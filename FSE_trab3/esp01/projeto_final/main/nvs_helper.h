#ifndef NVS_HELPER_H
#define NVS_HELPER_H

void setup_nvs();

bool nvs_read_int_value(const char * key, int * value);

bool nvs_write_int_value(const char * key, int value);

#endif
