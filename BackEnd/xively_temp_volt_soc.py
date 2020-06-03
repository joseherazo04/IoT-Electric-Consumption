#!/usr/bin/python
# coding: utf-8

# Código para leer el valor del sensor de temperatura
# de la Raspberry PI y enviar los valores leídos a la
# plataforma xively 

import os
import xively
import serial
import datetime

# Variables del dispositivo dadas por la plataforma xively
FEED_ID = "XXXX"
API_KEY = "XXXX"

# Inicializar Cliente API
api = xively.XivelyAPIClient(API_KEY)

# Funcion para obtener el valor de la temperatura del SoC
def getTemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Funcion para obtener el valor del voltaje del nucleo de la RPI
def getVolts():
    res = os.popen('vcgencmd measure_volts core').readline()
    return(res.replace("volt=","").replace("V\n",""))

# Funciones para crear los Canales en xively (Datastreams)

# Funcion para crear canal de datos de Temperatura
def create_datastreams_temp(feed):
   try:
      datastream = feed.datastreams.get("Temperatura")
      return datastream
   except:
      datastream = feed.datastreams.create("Temperatura", tags="C")
      return datastream
    
# Funcion para crear canal de datos de Voltaje
def create_datastreams_volts(feed):
   try:
      datastream = feed.datastreams.get("Voltaje")
      return datastream
   except:
      datastream = feed.datastreams.create("Voltaje", tags="volts")
      return datastream

# Funcion para crear canal de datos de Power1
def create_datastreams_power1(feed):
   try:
      datastream = feed.datastreams.get("Power1")
      return datastream
   except:
      datastream = feed.datastreams.create("Power1", tags="Watts")
      return datastream

    # Funcion para crear canal de datos de Power2
def create_datastreams_power2(feed):
   try:
      datastream = feed.datastreams.get("Power2")
      return datastream
   except:
      datastream = feed.datastreams.create("Power2", tags="Watts")
      return datastream

feed = api.feeds.get(FEED_ID)

#Crea canales llamando a las funciones
canalvolts= create_datastreams_volts(feed)
canaltemp= create_datastreams_temp(feed)
canalpower1= create_datastreams_power1(feed)
canalpower2= create_datastreams_power2(feed)


#Se leen los valores del sistema
temp = getTemp()
volts = getVolts()


#actualizar valores de los canales
canaltemp.current_value = temp
canalvolts.current_value = volts

#Lectura de los valores de los sensores CT
ser = serial.Serial('/dev/ttyAMA0', 38400, timeout=1)
response = ser.readline() 
z = response.split(" ")

#Calculo de las potencias
if len(z)>=6:
    #potencias decodificadas
    p1=float((float(z[3])* 256.0 + float(z[2])))
    p2=float((float(z[5])* 256.0 + float(z[4])))
    #consumo recalculado a 120 V
    power1=p1*0.5
    power2=p2*0.5
    canalpower1.current_value = power1
    canalpower2.current_value = power2

#Asignar fecha y hora de actualizacion
canaltemp.at = datetime.datetime.utcnow()
canalvolts.at = datetime.datetime.utcnow()
canalpower1.at = datetime.datetime.utcnow()
canalpower2.at = datetime.datetime.utcnow()

#Se envìa la peticion de actualizacion a servidor xively 
canaltemp.update()
canalvolts.update()
canalpower1.update()
canalpower2.update()


