import socket               # Import socket module
from gopigo import *	#Has the basic functions for controlling the GoPiGo Robot
import sys	#Used for closing the running program
import pygame #Gives access to KEYUP/KEYDOWN events
import picamera
import os, os.path
import numpy as np
import argparse
import os
import sys
camera=picamera.PiCamera()
charpre='p'
accelerate=0

if __name__ == '__main__':
    iteration=0
    while True:
        imagename='/home/pi/Desktop/capture.jpg'
        camera.capture(imagename)
        s = socket.socket()         # Create a socket object
        host = '192.168.1.15' # Get local machine name
        port = 12344                 # Reserve a port for your service.

        
        s.connect((host, port))
        f = open('capture.jpg','rb')
        print 'Sending...'
        l = f.read(1024)
        while (l):
            print 'Sending...'
            s.send(l)
            l = f.read(1024)
        f.close()
        print "Done Sending"
        s.shutdown(socket.SHUT_WR)

        
        char=s.recv(1024)
        print('character received is ',char)
        s.close()

        if char=='w':
                    motor1(1,100)
                    motor2(1,100)
                    print('running in w')
                    time.sleep(0.5)
                    motor1(1,0)
                    motor2(1,0)
        elif char=='a':
                    motor1(1,130+accelerate)
                    motor2(1,100)

                    time.sleep(0.5)
                    
                    motor1(1,100)
                    motor2(1,100)
                    
                    motor1(1,0)
                    motor2(1,0)

                    
                    print('running in a')
                    
                     
                    
        elif char=='d':
                    #right();# Turn Right
                    motor1(1,100)
                    motor2(1,130+accelerate)

                    time.sleep(0.5)

                    motor1(1,100)
                    motor2(1,100)
                    
                    motor1(1,0)
                    motor2(1,0)
                    print('running in d')
                  
                    
        elif char=='s':
                    motor1(0,100)
                    motor2(0,100)
                    print('running in s')
                    time.sleep(0.5)
                    
        elif char=='t':
                    increase_speed();	# Increase speed
                    print('running in t')
        elif char=='g':
                    decrease_speed();	# Decrease speed
                    print('running in g')
           
            
        if (charpre==char) and (charpre=='a' or charpre=='d'):
               accelerate=accelerate+5
        else:
               accelerate=0
        charpre=char
        print('acceleration is ',accelerate)
        iteration=iteration+1



        
