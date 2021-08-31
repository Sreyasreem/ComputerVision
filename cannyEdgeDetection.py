#QUESTION 1: Canny Edge Detector algorithm

#Three different sigma values have been chosen.
#The algorithm works better with the lowest sigma value. With increasing sigma value, the fine edges of the image almost disappears.
#On execution, the program asks for 3 filenames one after the other. It yields three images for three different sigma values for a particular file. 
#Each image contains seven subplots, including the final image obtained after hysteresis method.

#Imporing the required libraries
from PIL import Image
import numpy as np
from pylab import *
from scipy import signal as sg
from math import*
import matplotlib.pyplot as plt	

#setting three different values for sigma
SD = [0.79,1.1,1.19]

#value of the filter length
filterLength = 3

#Low Threshold
low = 10

#High Threshold
high = 20

#outerloop variable
j = 0

#the outermost loop is for prompting the user to input 3 files
while j<3:

    #prompt for the user to input the desired filename
    filename = raw_input('Enter a filename: ')
    
    #read the image into an array
    #files will be expected from the given specific path
    I = (array(Image.open('Desktop/pythonFiles/'+filename).convert('L')))
    
    #innerloop variable
    i = 0
    
    #the while loop is for processing with three different SDs
    while i<3:
        
        sigma = SD[i]
        
        #function to create 1D Convolution Mask
        def convolutionMask(filter_length,sigma):
            
            mid = filter_length/2
        
            #gaussian formulaization
            result=[(1/(sigma*math.sqrt(2*math.pi)))*(1/(math.exp((i**2)/(2*sigma**2)))) for i in range(-mid,mid+1)]    
            
            #returns the list containing the mask
            return result 
        
        #normalized the convolution mask
        G = [(convolutionMask(filterLength,sigma)/sum(convolutionMask(filterLength,sigma)))]
        
        #created 1D mask required for convolution
        mask = [[-1,0,1]]
        
        #first derivative of the Gaussian in the x direction
        Gx = sg.convolve(mask, G, 'same')
        
        
        #first derivative of the Gaussian in the y direction
        Gy = sg.convolve(np.reshape(mask,(filterLength,1)), G,'same')
        
        #x component image
        Ix = sg.convolve(I, G, 'same')
        
        #plotting the image
        plt.figure(filename+'_sigma = '+str(sigma))
        plt.subplot(241)
        plt.imshow(Ix,cmap=plt.cm.gray)
        
        #Y component image
        Iy = sg.convolve(I, np.reshape(G,(filterLength,1)), 'same')
        
        #plotting the image
        plt.figure(filename+'_sigma = '+str(sigma))
        plt.subplot(242)
        plt.imshow(Iy,cmap=plt.cm.gray)
        
        #x-component of I convolved with the derivative of the Gaussian
        Ixd = sg.convolve(Ix, Gx, 'same')
        
        #plotting the image
        plt.figure(filename+'_sigma = '+str(sigma))
        plt.subplot(243)
        plt.imshow(Ixd,cmap=plt.cm.gray)
        
        #y-component of I convolved with the derivative of the Gaussian
        Iyd = sg.convolve(Iy, Gy, 'same')
        
        #plotting the image
        plt.figure(filename+'_sigma = '+str(sigma))
        plt.subplot(244)
        plt.imshow(Iyd,cmap=plt.cm.gray)
        
        #magnitude
        Mxy = np.empty([len(Ixd),len(Ixd[0])])
        
        #nested loop to iterate over each pixel
        for x in range (0,len(Ixd)):
            for y in range (0,len(Ixd[0])):
                
                #computes the magnitude of the current pixel
                Mxy[x][y] = math.hypot(Ixd[x][y],Iyd[x][y])
        
        #plotting the image
        plt.figure(filename+'_sigma = '+str(sigma))
        plt.subplot(245)
        plt.imshow(Mxy,cmap=plt.cm.gray)
        
        #orientation(theta)       
        gradDir = np.empty([len(Ixd),len(Ixd[0])])
        
        #nested loop to iterate over each pixel
        for x in range (0,len(Ixd)):
            for y in range (0,len(Ixd[0])):
                
                #computes the orientation of the current pixel
                gradDir[x][y] = math.atan2(Iyd[x][y],Ixd[x][y])
                
        #rounding the angles to four directions, vertical, horizontal, left diagonal, and right diagonal
        for x in range (0,len(Ixd)):
            for y in range (0,len(Ixd[0])):
                
                #for horizontal alignment
                if (gradDir[x][y]<22.5 and gradDir[x][y]>=0) or \
                    (gradDir[x][y]>=157.5 and gradDir[x][y]<202.5) or \
                    (gradDir[x][y]>=337.5 and gradDir[x][y]<=360):
                    gradDir[x][y]=0
                
                #for right diagonal alignment  
                elif (gradDir[x][y]>=22.5 and gradDir[x][y]<67.5) or \
                    (gradDir[x][y]>=202.5 and gradDir[x][y]<247.5):
                        gradDir[x][y]=45
                
                #for vertical alignment       
                elif (gradDir[x][y]>=67.5 and gradDir[x][y]<112.5)or \
                    (gradDir[x][y]>=247.5 and gradDir[x][y]<292.5):
                        gradDir[x][y]=90
                
                #for left diagonal alignment     
                else:
                    gradDir[x][y]=135   
        
                        
        #applying non-maximal suppression 
        for x in range (1,len(Ixd)-1):
            for y in range (1,len(Ixd[0])-1):
                
                #if the alignment is horizontal
                if gradDir[x][y]==0:
                    
                    #if the magnitude value current pixel is less than its neighbors, then set it to zero          
                    if (Mxy[x][y]<Mxy[x-1][y]) or \
                        (Mxy[x][y]<Mxy[x+1][y]):
                        Mxy[x][y]=0
                
                #if the alignment is left diagonal               
                elif gradDir[x][y]==135:
                    
                    #if the magnitude value current pixel is less than its neighbors, then set it to zero
                    if (Mxy[x][y]<Mxy[x-1][y+1]) or \
                        (Mxy[x][y]<Mxy[x+1][y-1]):
                        Mxy[x][y]=0
                
                #if the alignment is vertical               
                elif gradDir[x][y]==90:
                    
                    #if the magnitude value current pixel is less than its neighbors, then set it to zero
                    if (Mxy[x][y]<Mxy[x][y-1]) or \
                        (Mxy[x][y]<Mxy[x][y+1]):
                        Mxy[x][y]=0
                
                #if the alignment is right diagonal               
                elif gradDir[x][y]==45:
                    
                    #if the magnitude value current pixel is less than its neighbors, then set it to zero
                    if (Mxy[x][y]<Mxy[x+1][y+1]) or \
                        (Mxy[x][y]<Mxy[x-1][y-1]):
                        Mxy[x][y]=0
        
        #plotting the image
        plt.figure(filename+'_sigma = '+str(sigma))          
        plt.subplot(246)
        plt.imshow(Mxy,cmap=plt.cm.gray)
        
        #creating an array for hysteresis
        hysteresisTH = np.empty([len(Ixd),len(Ixd[0])]) 
        
        #edge pixel=1
        #non-edge pixel = 0
        
        #applying hysteresis thresholding
        
        for x in range (0,len(Ixd)):
            for y in range (0,len(Ixd[0])):
                
                #checking for an edge pixel
                if Mxy[x][y] > high:
                    hysteresisTH[x][y] = 1
                
                #checking for a non-edge pixel   
                elif Mxy[x][y] < low:
                    hysteresisTH[x][y] = 0
                
                #filling with a dummy value,2, if it is between high and low    
                else:
                    hysteresisTH[x][y] = 2
        
        #next step is to turn the pixels with dummy values as edge and non-edge pixel
        #we will use 4-connected neighbors to find an edge pixel
        flag = True
        
        #keep looping until we get all the edge pixels
        while flag:
            
            flag = False  
                    
            for x in range (1,len(Ixd)-1):
              for y in range (1,len(Ixd[0])-1):
                
                #if one of the neighbors is an edge pixel, then the current pixel becomes an edge pixel
                if hysteresisTH[x][y] == 2 and (hysteresisTH[x-1][y] == 1 or hysteresisTH[x+1][y] == 1 or hysteresisTH[x][y-1] == 1 or hysteresisTH[x][y+1] == 1):
                    hysteresisTH[x][y] = 1
                    flag = True
                    
        #assign the values accordingly in the final matrix           
        for x in range (0,len(Ixd)):
            for y in range (0,len(Ixd[0])):
                
                if hysteresisTH[x][y] == 2 or hysteresisTH[x][y] == 0:
                    Mxy[x][y] = 0 
        
        #plotting the image
        plt.figure(filename+'_sigma = '+str(sigma))            
        plt.subplot(247)
        plt.imshow(Mxy,cmap=plt.cm.gray)
        plt.show()
        
        i += 1
        
        #saving the ouput image so that it can be utilized for question 2
        finalImage = Image.fromarray(Mxy.astype(np.uint8))
        finalImage.save('Desktop/pythonFiles/'+filename.split('.')[0]+'cannyEdgeOut_sigma'+str(sigma)+'.png')#filename.split('.')[1])
        
    j += 1
