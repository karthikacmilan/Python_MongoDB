#!/usr/bin/python2.7
#
# Assignment5 Interface
# 
#

from pymongo import MongoClient
import os
import sys
import json
import re
from math import sin, cos, sqrt, atan2, radians
import math

#The file contains the code for the Assignment5 FindBusinessBasedOnCity & FindBusinessBasedOnLocation. 
 
# Python 2.7.6 & MongoDB 3.0.7
 
# Input data : testData.json
 
# Output : findBusinessBasedOnCity.txt and findBusinessBasedOnLocation.txt


def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
    #Reference : https://docs.python.org/2/library/re.html ( re.I Ignorance case ) 
    #TestCase : "Tempe" failed so making it case insensitive 
    formattedInput=re.compile("^"+cityToSearch+"$",re.I)
    #Reference : http://api.mongodb.org/python/current/api/pymongo/collection.html 
    a=collection.find({"city":formattedInput})
    file = open(saveLocation1, "w")
    for value in a:
    #removing \n from full_address 
    #Reference : http://www.tutorialspoint.com/python/string_replace.htm
    file.write(value['name'].upper()+'$'+value['full_address'].upper().replace('\n'," ")+'$'+value['city'].upper()+'$'+value['state'].upper()+'\n')
    file.close()
    pass

def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
    categoriesToSearchArray=[]
    file = open(saveLocation2, "w")
    for cat in categoriesToSearch:
        categoriesToSearchArray.append(re.compile("^"+cat+"$",re.I))
    a=collection.find({"categories":{"$in":categoriesToSearchArray}})
    for value in a:
    #convert string to float for the value in latitude & longitude
    calculation =  Distance(float(myLocation[0]),float(myLocation[1]),value['latitude'],value['longitude'])
        if calculation <= maxDistance:
        #Reference : http://stackoverflow.com/questions/15092437/python-encoding-utf-8
        file.write(value['name'].upper().encode('utf8')+'\n')
    file.close()
    pass

def Distance(a,b,c,d):
    #The distance returned would be in miles. [lat1, lon1] and [lat2, lon2] are two different coordinates
    
    R = 3959; #miles
    Lata = radians(a)
    Latc = radians(c)
    Latb = radians(d - b)
    Latd = radians(Latc - Lata)

    w = pow((sin(Latd/2)),2) + cos(Lata) * cos(Latc) * pow((sin(Latb/2)),2)
    y = 2 * atan2(sqrt(w), sqrt(1-w))
    z = R * y
    return z


