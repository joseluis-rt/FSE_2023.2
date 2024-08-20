set(COMPONENT_SRCS "main.c" "lib/buzzer.c" "lib/dht.c" "lib/wifi.c" "lib/mqtt.c")
set(COMPONENT_ADD_INCLUDEDIRS ".")
                    
register_component()
component_compile_options(-Wno-error=format= -Wno-format)

