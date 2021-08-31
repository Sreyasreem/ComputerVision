#QUESTION 3
#This program uses Entropy information for mapping image intensity values into two classes: white (foreground) and black (background).

    
#importing the required libraries
from PIL import Image
import numpy as np
from pylab import *
import math
    
#set possible gray levels
L = 256
    
#loop variable
i=0

#the while loop is for reading three gray scale images and plotting the respective binary images    
while i<3: 
    
    #prompt for the user to input the desired filename
    filename = raw_input('Enter a filename: ')
       
    #read the image into an array
    I = (array(Image.open('Desktop/pythonFiles/'+filename).convert('L')))
    
    #plotting the gray scale image
    plt.figure(str(i+1)+' : '+filename)  
    plt.subplot(121)          
    plt.imshow(I,cmap=plt.cm.gray)
    plt.show()
    
    #computes the size of the image matrix
    Total_pixels = len(I)*len(I[0])
    
    
    #list to store the frequency of intensities ranging from 0 to 255
    freqM = np.zeros(L, dtype=int)
    
    #a particular @index in the list, freqM, stores the frequency of the intensity @index
    #example: freqM[5] contains the frequency of Intensity 5, that is, number of pixels that has Intensity 5
    for x in range (0,len(I)):
        for y in range (0,len(I[0])):
            
            #On finding a particular intensity, that particular index is the list, freqM, gets incremented by 1
            freqM[I[x][y]] += 1
    
    
    #finds the pdf of @index
    def find_pdf(index):
        return float(freqM[index])/Total_pixels
        
    
    #summation of pdfs until a certain threshold, T 
    def summationThreshold(T):  
        
        #initially, sum is set to zero
        sum = 0
        
        #summing up the frequencies starting at zero until @T
        while T >= 0:
            sum += freqM[T]
            T -= 1
        
        #returns the summations of the pdfs    
        return float(sum)/Total_pixels
        
    
    #list to store the total entropy at thresholds ranging from 1 to 255
    maxTot_Ent = np.zeros(L)
    
    def totalEntropy():
        
        #loop to iterate over each threshold and find the one that causes the maximum entropy
        for T in range (1,L):
            
            #entropy of region A initially set to zero 
            sum_A = 0
            
            #entropy of region B initially set to zero 
            sum_B = 0
            
            #computes the entropy for the region A
            for x in range (0,T+1):
                
                if summationThreshold(T) != 0:
                    h = find_pdf(x)/summationThreshold(T)
                
                #check statement to avoid the error when number of pixels is zero of a particular intensity
                    if h != 0:
                      sum_A += -(h*math.log10(h))
            
            #computes the entropy for the region B 
            for y in range (T+1,L):
                
                #check statement to avoid float division by zero error 
                if summationThreshold(T) != 1:
                    h = find_pdf(y)/(1-(summationThreshold(T)))
                
                #check statement to avoid the error when number of pixels is zero of a particular intensity
                    if h != 0:
                       sum_B += -(h*math.log10(h))
            
            #computes the total entropy          
            maxTot_Ent[T] = sum_A + sum_B
        
        return maxTot_Ent
    
    #invokes the function to find the threshold that causes the maximum total entropy                    
    totalEntropy() 
    
    #finds the index which contains the largest total entropy
    max_T = maxTot_Ent.tolist().index(max(maxTot_Ent))
    
    #binary matrix
    O = np.empty([len(I),len(I[0])])
    
    #for constructing the binary matrix
    for x in range (0,len(I)):
        for y in range (0,len(I[0])):
            
            #checking if the current pixel is greater than the set Threshold
            if I[x][y] >= max_T:
                O[x][y] = 1
    
    
    print 'The max threshold is: ',max_T
    
    #plotting the binary image
    plt.figure(str(i+1)+' : '+filename)   
    plt.subplot(122)          
    plt.imshow(O,cmap=plt.cm.gray)
    plt.show()
    
    i += 1