#QUESTION 2a

#Out1 is the ground truth image and finalIm is the final image out of my cany edge detector algorithm
#NOTE: For simplicity, please make sure the way you save your ground truth has the same dimension as your original image.
#iMPORTANT NOTE:For example, if the your original image,which you will through my canny edge detector algorithm, is 481x321, then your ground truth SHOULD be 481x321 AS WELL and NOT 321X481. If the original image is longer vertically, make sure the ground truth image is also longer vertically and not horizontally.
#NOTE:If the above criteria is not maintained, then this algorithm will generate index out of bound error. 
#NOTE:If you don't follow the dimensionality rule and use resize(), the accuracy will be decreased.
#NOTE:Hence, please maintain the proper dimensions for the ground truth image and original image.

#importing the required libraries
from PIL import Image
import numpy as np
from pylab import *
from scipy import signal as sg
import matplotlib.pyplot as plt	

#Initially setting true positive, false negative, true negative, and false positive to zero
TP = FN = TN = FP = 0

# reads the ground truth image into an array
Out1 = (array(Image.open('Desktop/pythonFiles/output_image.png').convert('L')))

# reads the desired output image from my canny edge detector algorithm into an array
finalIm = (array(Image.open('Desktop/pythonFiles/input_imagecannyEdgeOut_sigma0.79.png').convert('L')))

#comparison takes place between my output image from canny edge algorithm and ground truth for every pixel
for x in range (0,len(finalIm)):
    for y in range (0,len(finalIm[0])):
        
        #checking and determining true positives
        if finalIm[x][y] != 0 and Out1[x][y] != 0:
            TP += 1
        
        #checking and determining false negatives    
        elif finalIm[x][y] == 0 and Out1[x][y] != 0:
            FN += 1
        
        #checking and determining true negatives   
        elif finalIm[x][y] == 0 and Out1[x][y] == 0:
            TN += 1
        
        #false positives    
        else:
            FP += 1

#computing the required data 
#formulae have been provided in the assignment      
Sensitivity = float(TP)/(TP+FN)
Specificity = float (TN)/(TN+FP)
Precision = float(TP)/(TP+FP)
Negative_Predictive_Value = float(TN)/(TN+FN)
Fall_out = float(FP)/(FP+TN)
False_Negative_Rate = float(FN)/(FN+TP)
False_Discovery_Rate = float(FP)/(FP+TP)
Accuracy = float(TP+TN)/(TP+FN+TN+FP)
F_score = float (2*TP)/((2*TP)+FP+FN)
Matthew_Correlation_Coefficient = float((TP*TN) - (FP*FN))/(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))

#displaying the results
print 'Sensitivity: ',Sensitivity
print 'Specificity: ',Specificity
print 'Precision: ',Precision
print 'Negative_Predictive_Value: ',Negative_Predictive_Value
print 'Fall_out: ',Fall_out
print 'False_Negative_Rate: ',False_Negative_Rate
print 'False_Discovery_Rate: ',False_Discovery_Rate
print 'Accuracy: ',Accuracy
print 'F_score: ',F_score
print 'Matthew_Correlation_Coefficient: ',Matthew_Correlation_Coefficient           