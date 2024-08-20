set(COMPONENT_SRCS "led_rgb.c" "nvs_helper.c" "flame_detector.c" "main.c" "mqtt.c" "main.c" "wifi.c" "cJSON.c")
set(COMPONENT_ADD_INCLUDEDIRS ".")
                    
register_component()
component_compile_options(-Wno-error=format= -Wno-format)