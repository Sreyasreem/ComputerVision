# -*- coding: utf-8 -*-
#QUESTION 4c: Harris Corner Detection with a different cornerness

#This cornerness is less efficient (takes more time to execute) than the cornerness given in the 2nd question. 


#importing the required libraries
from PIL import Image
import numpy as np
from pylab import *
from scipy import signal as sg
from math import*
import time

#value of the Standard Deviation
sigma = 1.1

#value of the filter length
filterLength = 5

#setting the alpha value
alpha = 1.0/25

#list containing the files to be processed
files = ['input1.png','input2.png','input3.png']

#loop variable
i = 0

#the outer loop is for reading three files
while i<3:

    #gets the file located in the list,files,at @i
    filename = files[i]
    
    #reads the image into an array
    I = (array(Image.open('Desktop/pythonFiles/'+filename).convert('L')))
    
    #function to create 1D Convolution Mask
    def convolutionMask(filter_length,sigma):
    
        mid = filter_length/2
        
        #creating the mask with the gaussian formula
        result=[(1/(sigma*math.sqrt(2*math.pi)))*(1/(math.exp((i**2)/(2*sigma**2)))) for i in range(-mid,mid+1)]    
            
        return result 
    
    #normalized the convolution mask
    G = [(convolutionMask(filterLength,sigma)/sum(convolutionMask(filterLength,sigma)))]
    
    #1D mask for the first derivative
    mask = [[-2,-1,0,1,2]]
    
    #smoothed the image
    L = sg.convolve(I, G, 'same')
    
    #first derivative in the x direction
    Lx = sg.convolve(L, mask, 'same')
    
    #first derivative in the y direction
    Ly = sg.convolve(L, np.reshape(mask,(filterLength,1)), 'same')
    
    #computes the square root of the discriminant of the quadratic equation
    def find_disc(a,b,c):
        return math.sqrt((b*b)-(4*a*c))
        
    #starting the timer
    start = time.time()
    
    #matrix for the first eigen value of every pixel
    eigen1 = np.empty([len(I),len(I[0])])
    
    #matrix for the second eigen value of every pixel
    eigen2 = np.empty([len(I),len(I[0])])
    
    #finds the two roots, eigen values, for every pixel    
    for x in range (0,len(I)):
        for y in range (0,len(I[0])):
    
            #a,b,c values are determined after solving A - lambda*I = 0
            #I is the 2x2 Identity matrix,lambda yields the 2 roots, and A is the H2 matrix given in the question
            a = 1
            b = -((Lx[x][y] ** 2) + (Ly[x][y] ** 2))
            c = 0 
            
            #root1
            eigen1[x][y] = float(-b + find_disc(a,b,c))/2
            
            #root2
            eigen2[x][y] = float(-b - find_disc(a,b,c))/2
    
    #matrix for the cornerness of every pixel
    harrisM = np.empty([len(I),len(I[0])])
    
    #nested loop to compute the cornerness of every pixel
    for x in range (0,len(I)):
        for y in range (0,len(I[0])):
            
            #computing the cornerness of the current pixel
            #Cornerness(p,σ,α) = λ1λ2 − α(λ1 + λ2)
            harrisM[x][y] = (eigen1[x][y] * eigen2[x][y]) - alpha * (eigen1[x][y] + eigen2[x][y]) 
            
    #plotting the image 
    plt.figure(str(i+1)+' : '+filename)       
    imshow(harrisM)
    show() 
    
    #displaying the time 
    print 'It took', time.time()-start, 'seconds.' 
    
    i += 1    