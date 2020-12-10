# 802dot11

Este proyecto fue creado para aprobar la materia "Comunicacion de datos" de la Maestria en Telecomunicaciones de la Universidad Nacional de Cordoba.


Se toman paquetes del protocolo 802.11 de utilizando una raspBerry Pi con una adaptador wifi usb. Esos paquetes son enviados a una PC mediante una conexion TCP utilizando sockets. Los paquetes son reenpaquetados y desempaquetados en la PC.
Luego de ser guardados en archivos se extrae la informacion correspondiente a nombre de red, intesidad de señal, ID de la RaspBerry y timestamp. Esta informacion es insertada en una base de datos InfluxDB.
Para la consulta web de los datos se utiliza un servidor Flask con un script que consulta a la DB y reporta el ultimo estado conocido de la red con su intensidad en dB.
