#ifndef MQTT_H
#define MQTT_H

void mqtt_start();

void mqtt_envia_mensagem(char * topico, char * mensagem);

void mqtt_request_attributes();

void enviar_comando_rpc(const char *id, const char *comando);


#endif