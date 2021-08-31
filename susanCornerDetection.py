#QUESTION 5: Susan Corner Detection

#1)threshold1 = 20 and threshold2 = 200 are the free parameters for susan_input1.png.TH=20 and th2=150 also workds well. g is taken half of the max n
#Both the images, susan_input1 and susan_input2 (noisy image) were passed through this algorithm.
#The corners were very well detected in both the images. The second image was very noisy, but the the corners were sharply detected.
#The script,preProcessIm.py, smoothes the noisy image, susan_input2.png. The output image can be passed through this algorithm for corner detection. One can just simply replace one of the files from the list,files, with smootheOut.png file and check the results.
#due to smoothing, a portion of 1-2 corners were slightly not detected.
#when detecting corners and dealing with noisy images, we can use susan detection algorithm. We can also use median_filter from scipy and import cv2 library and use various denoising functions, such as, cv2.fastNlMeansDenoising()


#importing the required libraries
from PIL import Image
import numpy as np
from pylab import *
from scipy import signal as sg
from math import *
import matplotlib.pyplot as plt

#threshold for plugging into the n(r) equation
TH = 20

#threshold for the comparison of intensity of the nucleus and its neighboring pixels that fall witin the mask
th2=150

#circular mask
susan_mask = [[0, 0, 1, 1, 1, 0, 0],
	      [0, 1, 1, 1, 1, 1, 0],
	      [1, 1, 1, 1, 1, 1, 1],
	      [1, 1, 1, 1, 1, 1, 1],
	      [1, 1, 1, 1, 1, 1, 1],
	      [0, 1, 1, 1, 1, 1, 0],
	      [0, 0, 1, 1, 1, 0, 0]]
	      

#list containing the files to be processed
files = ['susan_input1.png','susan_input2.png']

#loop variable
var = 0

#outer loop is used for processing two different files
while var<2:
    
    #prompt for the user to input the desired filename
    filename = files[var]
    
    #read the image into an array
    I = (array(Image.open('Desktop/pythonFiles/'+filename).convert('L'), dtype='int64'))
    
    #for storing n(r) of the pixels of the image matrix
    Nr = np.empty([len(I),len(I[0])])
    
    #for maximum n(r0)
    MAX_n = 0
    
    #find the significant pixels that are of comparable brightness to the current pixel
    #outer nested loops to iterate over the image matrix
    #the goal is to compute USAN for every pixel
    #for simplicity, I'm starting the iteration from I[3][3], because otherwise padding with zeros is required 
    for x in range (3,len(I)-4):
        for y in range (3,len(I[0])-4):
            
            #for n(r) of each pixel
            sum = 0.0
            
            #inner nested loop to iterate over the mask and find the corresponding pixels
            #we want to place the nucleus of the circular mask on the current pixel of the Image
            for i in range (x-3,x+4):
              for j in range (y-3,y+4): 
                
                #if the circular mask at this current location contains 1, then we want the comparison otherwise no
                if susan_mask[i-x+3][j-y+3] == 1:
                    
                    #checking for pixels with similar brightness from the corresponding pixels located in the mask
                    if I[i][j] - I[x][y] < th2:
                        
                        #computing the number of pixels of USAN
                        sum += math.exp(-1* math.pow((I[i][j] - I[x][y])/TH,6))
            
            #assigning the USAN for the current pixel            
            Nr[x][y] = sum
            
            #finds the maximum n(r)
            if Nr[x][y] > MAX_n:
                MAX_n = Nr[x][y]
                        
    
    #finds 'g' for the required computation            
    g = MAX_n/2
    
    
    #computation for the strength of a corner
    for x in range (0,len(I)):
        for y in range (0,len(I[0])):
            
            #checking if the current pixel is less than 'g'
            if Nr[x][y] <= g:
                Nr[x][y] = g - Nr[x][y]
                
                
    #Steps for applying Non-maximum suppression
    
    #value of the filter length
    filterLength = 3
    
    #created 1D mask required for convolution
    mask = [[-1,0,1]]
    
    #first derivative in the x direction
    Nrx = sg.convolve(Nr,mask, 'same')
    
    
    #first derivative in the y direction
    Nry = sg.convolve(Nr,np.reshape(mask,(filterLength,1)),'same')
    
    #matrix for magnitude of each pixel
    Mxy = np.empty([len(Nr),len(Nr[0])])
    
    #nested loop to iterate over each pixel of the Nr matrix
    for x in range (0,len(Nr)):
        for y in range (0,len(Nr[0])):
            
            #computes the magnitude of the current pixel
            Mxy[x][y] = math.hypot(Nrx[x][y],Nry[x][y])
    
    
    #matrix for orientation of each pixel       
    gradDir = np.empty([len(Nrx),len(Nrx[0])])
    
    #nested loop to iterate over each pixel of the Nr matrix
    for x in range (0,len(Nrx)):
        for y in range (0,len(Nrx[0])):
            
            #computes the orientation of the current pixel of Nr matrix
            gradDir[x][y] = math.atan2(Nry[x][y],Nrx[x][y])
            
    #rounding the angles to four directions, vertical, horizontal, left diagonal, and right diagonal
    for x in range (0,len(Mxy)):
        for y in range (0,len(Mxy[0])):
            
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
    for x in range (1,len(Mxy)-1):
        for y in range (1,len(Mxy[0])-1):
            
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
            
            #if the alignment is left diagonal              
            elif gradDir[x][y]==45:
                
                #if the magnitude value current pixel is less than its neighbors, then set it to zero
                if (Mxy[x][y]<Mxy[x+1][y+1]) or \
                (Mxy[x][y]<Mxy[x-1][y-1]):
                    Mxy[x][y]=0                        
        
    #plots the image
    plt.figure(str(var+1)+' : '+filename)
    plt.imshow(Mxy)
    plt.show()
    
    var += 1