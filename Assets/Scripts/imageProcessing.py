#!/usr/bin/python 
import cv2, numpy as np
import sys 

from DetectDarkZones import DetectDarkZones

fileName = str(sys.argv[1])

image = cv2.imread('F:\\Desarrollo\\PythonUnity\\Images\\'+fileName)
y, x, z = image.shape

darkZone = DetectDarkZones(50, x, y)
darkZone.detectZones(image)

image = darkZone.drawRectangle(image, (255,0,0))
image = darkZone.drawPercentage(image, (0,255,0))

print(darkZone.getDarkestZone())