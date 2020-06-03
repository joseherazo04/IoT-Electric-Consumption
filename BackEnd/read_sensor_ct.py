#!/usr/bin/python
# coding: utf-8

# Código para leer el valor del sensor de corriente
# de la Raspberry PI

import serial
import string
import ast

ser = serial.Serial('/dev/ttyAMA0', 38400, timeout=1)
#ser.open()

try:
        while 1:
                response = ser.readline()
                
                z = response.split(" ")
                
                if len(z)>=6:
                        print ("\n\n %s " % z)
                        #potencias decodificadas
                        p1=float((float(z[3])* 256.0 + float(z[2])))
                        p2=float((float(z[5])* 256.0 + float(z[4])))
                        #p3=float((float(z[7])* 256.0 + float(z[6])))

                        #consumo recalculado a 120 V
                        power1=p1*0.5
                        power2=p2*0.5
                        #power3=p3*0.5
                        
        
                        print ("Power 1: %s Watts" % power1)
                        print ("Power 2: %f Watts" % power2)
        
                        #print ("Power 3: %s Degrees" % power3)
                        
except KeyboardInterrupt:
        ser.close()

        #stty -F /dev/ttyAMA0 \raw speed 38400
#cat /dev/ttyAMA0

