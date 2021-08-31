from PIL import Image
import numpy as np
from pylab import *
from scipy import signal as sg
from math import*

#for randomly asigning numbers
import random	

#value of the Standard Deviation
sigma = 10

#value of the filter length
mean = 0

TP = FN = TN = FP = 0
# STEP1: read the image into an array
Out1 = array(Image.open('Desktop/pythonFiles/output_image.png'))


In1 = array(Image.open('Desktop/pythonFiles/input_image.jpg').convert('L'))

#Adding Gaussian noise
gaussianIm = In1 + np.random.normal(mean,sigma,In1.shape)

finalImage = Image.fromarray(gaussianIm.astype(np.uint8))
finalImage.save('Desktop/pythonFiles/gaussianIm.png')

#finalIm = (array(Image.open('Desktop/pythonFiles/final.png')))
#Checking for the various factors
#for x in range (0,len(In1)):
 #   for y in range (0,len(In1[0])):
        
 #       if finalIm[x][y] != 0 and Out1[x][y] != 0:
       ##     TP += 1
            
       ## elif finalIm[x][y] == 0 and Out1[x][y] != 0:
           # FN += 1
            
        #elif finalIm[x][y] == 0 and Out1[x][y] == 0:
            #TN += 1
            
        #else:
            #FP += 1
            
#Sensitivity = float(TP)/(TP+FN)
#Specificity = float (TN)/(TN+FP)
#Precision = float(TP)/(TP+FP)
#Negative_Predictive_Value = float(TN)/(TN+FN)
#Fall_out = float(FP)/(FP+TN)
#False_Negative_Rate = float(FN)/(FN+TP)
#False_Discovery_Rate = float(FP)/(FP+TP)
#Accuracy = float(TP+TN)/(TP+FN+TN+FP)
#F_score = float (2*TP)/((2*TP)+FP+FN)
#Matthew_Correlation_Coefficient = float((TP*TN) - (FP*FN))/(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))

#print 'Sensitivity: ',Sensitivity
#print 'Specificity: ',Specificity
#print 'Precision: ',Precision
#print 'Negative_Predictive_Value: ',Negative_Predictive_Value
#print 'Fall_out: ',Fall_out
#print 'False_Negative_Rate: ',False_Negative_Rate
#print 'False_Discovery_Rate: ',False_Discovery_Rate
#print 'Accuracy: ',Accuracy
#print 'F_score: ',F_score
#print 'Matthew_Correlation_Coefficient: ',Matthew_Correlation_Coefficient 