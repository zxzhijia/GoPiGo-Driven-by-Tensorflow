# GoPiGo Driven by Tensorflow
GoPiGo robot driven autonomously by trained CNN using retrained Tensorflow inception 3.

How to collection your own data:

Prerequisite:
Raspberry Pi Camera successfully setted
GoPiGo package installed
vnc

Steps:
1. remote connect your GoPiGo through ssh
```
ssh USERNAME@IP.ADDRESS
```

2. Start remote desktop control
```
tightvncserver
vncserver :1 -geometry 1920x1080 -depth 24
```
start Remote Desktop Viewer on your PC. Then login your GoPiGo.

3. Open a terminal using your Remote Desktop Viewer on GoPiGo
4. create a folder called ```Data```, and three subfolders called ```a, w, d``` respectively.
5. run ```python datacollection.py```
6. Control your GoPiGo to follow the "road" you've built using either white paper or other materials.
7. The images will be saved in ```a, w, d``` folders. 
8. Copy or scp your ```Data``` folder to PC or Laptop and trained them using inception @petewarden  [Tensorflow for Poets](https://petewarden.com/2016/02/28/tensorflow-for-poets/)


Run server.py on laptop or desktop with wifi by typing:
```
python server.py --model=LOCATION of YOUR .pb FILE --labels=LOCATION of YOUR .txt LABEL FILE
```   
What server code is doing:

1. create socket and listening. 

2. Build the trained network using .pb file and txt file.

3. run the network and output a label with either 'w' for go front, 'a' for go left, 'd' for turn right.

4. Send the output label to the client (GoPiGo) through TCP connection.

What client code is doing:

1. Capture an image in front and save it as jpg file. 

2. connect to the socket.

3. Send image to server.

4. Receive output command from server through TCP.

5. excute command to control the robot.

Run client.py on GoPiGo:
```
python client.py
```
