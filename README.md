# GoPiGo Driven by Tensorflow
GoPiGo robot driven autonomously by trained CNN using retrained Tensorflow inception 3.
Run server.py on laptop or desktop with wifi by typing:
   python server.py --model=LOCATION of the trained .pb file --labels=LOCATION of the trained label .txt file
   
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


