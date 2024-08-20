set(COMPONENT_SRCS "ir_receiver.c" "mqtt.c" "wifi.c" "main.c")
set(COMPONENT_ADD_INCLUDEDIRS ".")

register_component()
component_compile_options(-Wno-error=format= -Wno-format)