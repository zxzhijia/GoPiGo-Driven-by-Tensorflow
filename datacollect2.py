from gopigo import *	#Has the basic functions for controlling the GoPiGo Robot
import sys	#Used for closing the running program
import pygame #Gives access to KEYUP/KEYDOWN events
import picamera
import os, os.path

camera=picamera.PiCamera()

#Initialization for pygame
pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption('Remote Control Window')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

# Display some text
instructions = '''
                      BASIC GOPIGO CONTROL GUI

This is a basic example for the GoPiGo Robot control 

(Be sure to put focus on thi window to control the gopigo!)

Press:
      ->w: Move GoPiGo Robot forward
      ->a: Turn GoPiGo Robot left
      ->d: Turn GoPiGo Robot right
      ->s: Move GoPiGo Robot backward
      ->t: Increase speed
      ->g: Decrease speed
      ->z: Exit
''';
size_inc=22
index=0
for i in instructions.split('\n'):
	font = pygame.font.Font(None, 36)
	text = font.render(i, 1, (10, 10, 10))
	background.blit(text, (10,10+size_inc*index))
	index+=1

# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()
imageinxa=len([name for name in os.listdir('/home/pi/Desktop/GoPiGolocal/Data/a') if os.path.isfile(os.path.join('/home/pi/Desktop/GoPiGolocal/Data/a',name))]) 
imageinxw=len([name for name in os.listdir('/home/pi/Desktop/GoPiGolocal/Data/w') if os.path.isfile(os.path.join('/home/pi/Desktop/GoPiGolocal/Data/w',name))]) 
imageinxd=len([name for name in os.listdir('/home/pi/Desktop/GoPiGolocal/Data/d') if os.path.isfile(os.path.join('/home/pi/Desktop/GoPiGolocal/Data/d',name))]) 
print(imageinxd)
file=open("keyboard","w")
charpre='p'
accelerate=0
while True:
	event = pygame.event.wait();
        pygame.event.clear();
        print('waiting for event')
	if (event.type == pygame.KEYUP):
		motor1(1,0)
                motor2(1,0)
                char='n'
                print('running in keyup')
		continue;
	if (event.type != pygame.KEYDOWN):
                char='n'
                print('running in key down')
		continue;	
	char = event.unicode;
	if char=='w':
                imagename='/home/pi/Desktop/GoPiGolocal/Data/'+char+'/'+str(imageinxw)+'.jpg'
                imageinxw=imageinxw+1
                camera.capture(imagename)
		motor1(1,100)
                motor2(1,100)
                print('running in w')
                time.sleep(0.5)
                motor1(1,0)
                motor2(1,0)
	elif char=='a':
                imagename='/home/pi/Desktop/GoPiGolocal/Data/'+char+'/'+str(imageinxa)+'.jpg'
                imageinxa=imageinxa+1
                camera.capture(imagename)
		#left();	# Turn left
                motor1(1,130+accelerate)
                motor2(1,100)

                time.sleep(0.5)
                
                motor1(1,100)
                motor2(1,100)
                
                motor1(1,0)
                motor2(1,0)

                
                print('running in a')
                
                 
                
	elif char=='d':
                imagename='/home/pi/Desktop/GoPiGolocal/Data/'+char+'/'+str(imageinxd)+'.jpg'
                imageinxd=imageinxd+1
                camera.capture(imagename)
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

                imagename='/home/pi/Desktop/GoPiGolocal/Data/'+char+'/'+str(imageinxs)+'.jpg'
                imageinxs=imageinxs+1
                camera.capture(imagename)
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
	elif char=='z':
		print "\nExiting";		# Exit
                file.close()
		sys.exit();

        file.write(char+"\n")
       
        
        if (charpre==char) and (charpre=='a' or charpre=='d'):
           accelerate=accelerate+5
        else:
           accelerate=0
        charpre=char
        print('acceleration is ',accelerate)
        

