#!/usr/bin/env bash

#verifico si existe la interface mon0 que usa collector
iw dev
devWifi=`iw dev | grep ^phy# | awk '{print $1}'`
echo "Se encontraron los siguientes dispositivos de hardware: "
echo $devWifi
unset devWifi
read -p "seleccione el dispositivo a utilizar para capturar los paquetes: "  devWifi
msg=$(iw dev | grep ^phy# | awk '{print $1}' | grep $devWifi)
if [ -z  $msg ]
then
    echo "el dispositivo:  $devWifi no existe"
    exit 1;
fi
devWifi=`echo $devWifi | sed 's/\#//g'`
echo "agregando interface monitor mon0 en device $devWifi ..."
res=`iw phy $devWifi interface add mon0 type monitor`
if [ -z  $res ]
then
    echo "interface agregada exitosamente"
    echo "iniciando servicio"
    unset res
    res=`ifconfig mon0 up`
    if [ -z  $res ]
    then
        echo "servicio iniciado"
    else
        echo "no pudo iniciar el servicio"
    fi
else
    echo "no pudo agregarse la interface mon0"
fi
