#!/usr/bin/python
# coding: utf-8

# Código para leer el valor del sensor de temperatura
# de la Raspberry PI y enviar los valores leídos a la
# plataforma xively 

import os
import xively
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

# Funcion para crear los Canales en xively (Datastreams)
def create_datastreams(feed):
   try:
      datastream = feed.datastreams.get("Temperatura")
      return datastream
   except:
      datastream = feed.datastreams.create("Temperatura", tags="temp")
      return datastream

feed = api.feeds.get(FEED_ID)
canal1= create_datastreams(feed)
temp = getTemp()
canal1.current_value = temp
canal1.at = datetime.datetime.utcnow()
canal1.update()