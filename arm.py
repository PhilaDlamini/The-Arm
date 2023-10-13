import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt 
import time
import numpy as np
import math

broker_address='67.253.32.232'
client = mqtt.Client('phila') 
client.connect(broker_address)

#Sends the angles and also displays positions on screen 
def plot_and_send(theta1, theta2, d, ax):
    x = [0, 0, 0]
    y = [0, 0, 0]
    x[1] = x[0] + d * math.cos(theta1)
    y[1] = y[0] + d * math.sin(theta1)
    x[2] = x[1] + d * math.cos(theta1 + theta2)
    y[2] = y[1] + d * math.sin(theta1 + theta2)
    ax.plot(x,y)
    
    #Also send the angles
    data = '(' + str(np.rad2deg(theta1)) + ', ' + str(np.rad2deg(theta2)) + ')'
#     print(data)
    client.publish('ME035', data)
    
#Arm length
d = 10
radius = d / 2
    
#Generate the cordinates for the points on circle (x - d) ^ 2 + y^2 = radius ^ 2
num_points = 50
angles = np.linspace(0, 2 * np.pi, num_points) #arr of angles from 0 to 2*pi
x_es = d + radius * np.cos(angles)
y_es = radius * np.sin(angles)

#Create a figure for all the points
fig, ax = plt.subplots()
ax.set(xlabel='X position', ylabel='Y position', title='Arm position')
ax.grid()
client.publish('light', 4)

# Calculate the angles for each point
for i in range(len(x_es)):
    x, y = x_es[i], y_es[i]
    
    #first angle 
    l = math.sqrt(x**2 + y**2)
    alpha = math.atan2(y, x)
    cos_g = (d**2 + l**2 - d**2) / (2*d*l)
    gamma = math.atan2(math.sqrt(1 - cos_g ** 2), cos_g)
    theta1 = gamma + alpha
    
    #second angle 
    cos_beta = (d**2 + d**2 - l**2) / (2*d*d)
    beta = math.atan2(math.sqrt(1 - cos_beta**2), cos_beta)
    theta2 = - math.pi + beta
    plot_and_send(theta1, theta2, d, ax)
    
plt.show()
client.disconnect()

        