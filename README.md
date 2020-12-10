# 802dot11

Este repositorio fue creado como proyecto final para aprobar la materia "Comunicacion de datos" de la Maestria en Telecomunicaciones de la Universidad Nacional de Cordoba.
En esta prueba de concepto desarrollamos un sistema de software para el monitoreo remoto de Access Points (APs) de redes inalámbricas de área local (WLANs) IEEE 802.11, con el que se colectan parámetros básicos de capa física (PHY) como también de la capa de acceso al medio (MAC).
El sistema consta de un dispositivo raspberry pi en modo monitor que guarda en archivos pcap los Beacon Frames (BFs) transmitidos por los APs,  estos BFs son enviados mediante una comunicación por socket a un servidor remoto, e insertados en una base de datos. A través de un servicio web es posible la visualización del identificador del servicio de red (SSID), intensidad de la señal recibida (RSSI), dirección física (MAC address), marca temporal (timestamp), y canal (channel) recibidos, además la información visualizada puede ser en valores instantáneos o históricos.
Las mediciones fueron realizadas de manera Indoor en ambiente no controlado.
