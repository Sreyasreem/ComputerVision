#Imporing the required libraries
from PIL import Image
import numpy as np
from pylab import *
from scipy import signal as sg
from scipy import linalg as lg
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
#import cv2


#files will be expected from the given specific path
I1 = (array(Image.open('Desktop/pythonFiles/basketball1.png').convert('L')))

#files will be expected from the given specific path
I2 = (array(Image.open('Desktop/pythonFiles/basketball2.png').convert('L')))

w = 5

kernel = [[-1/12.0,8/12.0,0,-8/12.0,1/12.0]]

timeKernel = [[-1,1]]

Ix = sg.convolve(I1,kernel,'same')
Iy = sg.convolve(I1, np.reshape(kernel,(5,1)), 'same')

It = sg.convolve(I1, timeKernel, 'same') + sg.convolve(I2, timeKernel, 'same')

u = np.empty([len(I1),len(I1[0])])
v = np.empty([len(I1),len(I1[0])])
#A = np.empty([w*w,2])
#b = np.empty([w*w,1])

#Ix_q = []
#Iy_q = []
#It_q = []

for x in range (2,len(I1)-w):
    for y in range (2,len(I1[0])-w):
        
        A = np.empty([w*w,2])
        b = np.empty([w*w,1])

        Ix_q = []
        Iy_q = []
        It_q = []
        
        #computation for each pixel
        for i in range (x-2,x+3):
           for j in range (y-2,y+3):
               
              Ix_q.append(Ix[i][j])
              Iy_q.append(Iy[i][j])
              It_q.append(It[i][j])
        
        #assigning the values into the required matrices      
        for z in range (0,len(Ix_q)):
            A[z][0] = Ix_q[z]
            A[z][1] = Iy_q[z]
            b[z][0] = -It_q[z]
        
        #matrix multiplication
        nu = np.dot(lg.pinv(A),b)
        
        u[x][y] = nu[0][0]
        v[x][y] = nu[1][0]

imshow(I1)
plt.hold(True)
        
for i in range (0,len(I1)):
    for j in range (0,len(I1[0])):
        
        if u[i][j] > 0 and v[i][j] > 0:
            plt.quiver(u,v,color='red')
            
show()
'''        
imshow(I1)
plt.hold(True)
plt.quiver(u,v,color='red',arrowstyle='->')
show()
'''        
#print u
print '****************************'
#print v            
        
