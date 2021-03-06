#!/usr/bin/env python3

"""
--------------------------------------------------------------------------------------
Created on  : 20 March 2019
Author      : Jusnaini
Descriptions:
         Read data from CropCircle sensor
         Serial port command to display data on terminal:
                sudo chmod o+rw /dev/ttyS#
                sudo stty -F /dev/ttyS# 38400 raw -echo
                sudo cat /dev/ttyS#
         If permission denied, consider to change port mode to 777
--------------------------------------------------------------------------------------
"""
import serial
import sys
#from datetime import datetime
import datetime
import numpy as np
import pandas as pd
import random


def vegetation_index(data):
    # unpack and split data into crop circle variables
    re,nir,red,ndre,ndvi = map(float,data.split(','))
    # derived other vegetation index
    rdvi    = (nir - red)/((nir+red)**0.5)
    redvi   = nir - re
    rerdvi  = (nir-re)/((nir+re)**0.5)
    resavi  = (1/5)*((nir-re)/(nir+re+0.5))

    #idx_list = [re,nir,red,ndre,ndvi,rdvi,redvi,rerdvi,resavi]
    idx_list = "%.3f,%.3f,%.3f,%.3f,%.3f," \
               "%.3f,%.3f,%.3f,%.3f" \
               % (re,nir,red,ndre,ndvi,rdvi,redvi,rerdvi,resavi)
    #print(*idx_list,sep=',\t')
    #print(idx_list)
    return(idx_list)

# Configure the serial port and open/activate it
ser = serial.Serial(
    port      = '/dev/ttyS8',
    baudrate  = 38400,
    parity    = serial.PARITY_NONE,
    stopbits  = serial.STOPBITS_ONE,
    bytesize  = serial.EIGHTBITS,
    timeout   = 1,
    xonxoff   = False,
    dsrdtr    = False,
    rtscts    = False,
    writeTimeout = None
)

get_filename = input('Filename : ')
f = open(get_filename+'.csv',"w+")
header = "Datetime,RedEdge,NIR,Red,NDRE,NDVI,RDVI,REDVI,RERDVI,RESAVI"
if ser.isOpen():
    try:
        f.write(header+'\n')

        while True:
            duration = 1
            time_start = datetime.datetime.now()
            time_end = time_start + datetime.timedelta(seconds=duration)

            while datetime.datetime.now() < time_end:
                data = ser.readline().decode()
                data_list = vegetation_index(data)
            print(type(data_list))
            f.write(datetime.datetime.now().isoformat()+'\t'+data_list+'\n')
            print(datetime.datetime.now().isoformat() +'\t'+data_list+'\n')

    except Exception as e:
        print ("Error communicating..: " + str(e))
    except KeyboardInterrupt:
        print("KeyboardInterrupted")
        sys.exit(0)
    f.close()
ser.close()


