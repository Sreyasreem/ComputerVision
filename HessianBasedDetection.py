#QUESTION 4a: Corner Detection based on Hessian Matrix
#eigen values are calculated for each pixel in the image matrix to check against a given threshold 

#importing the required librraies
from PIL import Image
import numpy as np
from pylab import *
from scipy import signal as sg
from math import*

#value of the filter length
filterLength = 3

#threshold for comparison
TH = -40

#list containing the files to be processed
files = ['input1.png','input2.png','input3.png']

#loop variable
i = 0

#the outer loop is for prompting user to enter 3 files
while i<3:

    #gets the filename located at @i
    filename = files[i]
        
    #read the image into an array
    #files will be expected from the given specific path
    I = (array(Image.open('Desktop/pythonFiles/'+filename).convert('L')))
    
    #create the masks
    maskX = [[-1,0,1]]
    maskY = np.reshape(maskX,(filterLength,1))
    
    #first derivative in the x direction
    Ix = sg.convolve(I, maskX, 'same')
    
    #first derivative in the y direction
    Iy = sg.convolve(I, maskY, 'same')
    
    #second derivative w.r.t x
    Ixx = sg.convolve(Ix, maskX, 'same')
    
    #second derivative w.r.t y
    Iyy = sg.convolve(Iy, maskY, 'same')
    
    #a second derivative done by taking the derivative of the first derivative in x wrt y
    Ixy = sg.convolve(Ix, maskY, 'same')
    
    #matrix for the first eigen value of every pixel
    eigen1 = np.empty([len(I),len(I[0])])
    
    #matrix for the second eigen value of every pixel
    eigen2 = np.empty([len(I),len(I[0])])
    
    #computes the square root of the discriminant of the quadratic equation
    def find_disc(a,b,c):
        return math.sqrt((b*b)-(4*a*c))
    
    #finds the two roots, eigen values, for every pixel      
    for x in range (0,len(I)):
        for y in range (0,len(I[0])):
    
            #a,b,c values are determined after solving A - lambda*I = 0
            #I is the 2x2 Identity matrix,lambda yields the 2 roots, and A is the H1 matrix given in the question
            a = 1
            b = -(Ixx[x][y] + Iyy[x][y])
            c = (Ixx[x][y] * Iyy[x][y]) - (Ixy[x][y] ** 2)
            
            #root1
            eigen1[x][y] = float(-b + find_disc(a,b,c))/2
            
            #roo2
            eigen2[x][y] = float(-b - find_disc(a,b,c))/2
    
    #matrix for the marking the cornerness       
    hessianM = np.empty([len(I),len(I[0])])
    
    #nested loop to iterate over the eigen values of every pixel
    for x in range (0,len(I)):
        for y in range (0,len(I[0])):
            
            #if the two eigen values of every pixel is greater than the set threshold, then we have a corner
            if eigen1[x][y] > TH and eigen2[x][y] > TH:
               hessianM[x][y] = 255
    
    #displaying the image 
    plt.figure(str(i+1)+' : '+filename)        
    imshow(hessianM)
    show()
    
    i += 1
            