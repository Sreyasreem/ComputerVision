#QUESTION 2b

#Two types of noises,gaussian and salt-pepper, are added to the image. 
#The output will be used to pass through the canny edge detector algorithm and will be evaluated by edgeDetectorEval.py


#importing the required libraries
from PIL import Image
import numpy as np
from pylab import *
from scipy import signal as sg
from math import*
import random	

#value of the Standard Deviation
sigma = 10

#value of the mean
mean = 0

#reading the images twice for adding two types of noises
In1 = array(Image.open('Desktop/pythonFiles/input_image.jpg').convert('L'))
In2 = array(Image.open('Desktop/pythonFiles/input_image.jpg').convert('L'))

#matrix for randomly storing numbers from 0-19
sapRM = np.empty([len(In1),len(In1[0])])

for x in range (0,len(In1)):
    for y in range (0,len(In1[0])):
        
       #randomly assigning a number from the range to the current pixel 
       sapRM[x][y] = random.randint(0,19)

#nested loop to add salt-pepper noise
#We need to have 10% salt and pepper. So, I'm adding 5% salt and 5% pepper
for x in range (0,len(In1)):
    for y in range (0,len(In1[0])):
        
        #if the current pixel in the random matrix contains 0, probability of 0.05(5%),then assign 0 to the corresponding pixel in the image matrix
        #Adding 5% pepper
        if sapRM[x][y] == 0:
            In1[x][y] = 0
         
        #if the current pixel in the random matrix contains 19, probability of 0.05(5%),then assign 255 to the corresponding pixel in the image matrix  
        #Adding 5% salt     
        elif sapRM[x][y] == 19:
         In1[x][y] = 255


#adding gaussian noise
gaussianImNoise = In2 + np.random.normal(mean,sigma,In2.shape)

#saving the image with added gaussian noise
finalImage = Image.fromarray(gaussianImNoise.astype(np.uint8))
finalImage.save('Desktop/pythonFiles/gaussianImNoise.png')

#saving the image with added salt and pepper noise
finalImageSAP = Image.fromarray(In1.astype(np.uint8))
finalImageSAP.save('Desktop/pythonFiles/SAP.png')