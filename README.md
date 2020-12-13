# 802dot11

This Repository was created as final project of the subject "Data Comunication" of the MSC in Telecommuinications of UNC.

In this  PoC I developed a software system for remote access  points (Aps) monitoring of IEEE 802.11 wirless local area networks (WLANs). It collects basic parameters in physical (PHY) layer as well as medium access control (MAC) layer. This system allows through a raspberry pi device setted up in monitor mode to save pcap  files with beacon frames (BFs) transmitted by APs, these BFs are sent using a socket connection to a remote server and inserted in a database. A web service was implemented to visualize service set identifier (SSID), Received Signal Strength Indication (RSSI), media access control address (MAC address), timestamp, and Channel number. Also the information visualized can be instantaneous and historical. Measures were done in a not controlled indoor environment.


Este repositorio fue creado como proyecto final para aprobar la materia "Comunicacion de datos" de la Maestria en Telecomunicaciones de la Universidad Nacional de Cordoba.

En esta prueba de concepto desarrollamos un sistema de software para el monitoreo remoto de Access Points (APs) de redes inalámbricas de área local (WLANs) IEEE 802.11, con el que se colectan parámetros básicos de capa física (PHY) como también de la capa de acceso al medio (MAC).
El sistema consta de un dispositivo raspberry pi en modo monitor que guarda en archivos pcap los Beacon Frames (BFs) transmitidos por los APs,  estos BFs son enviados mediante una comunicación por socket a un servidor remoto, e insertados en una base de datos. A través de un servicio web es posible la visualización del identificador del servicio de red (SSID), intensidad de la señal recibida (RSSI), dirección física (MAC address), marca temporal (timestamp), y canal (channel) recibidos, además la información visualizada puede ser en valores instantáneos o históricos.
Las mediciones fueron realizadas de manera Indoor en ambiente no controlado.
