from gopigo import *	#Has the basic functions for controlling the GoPiGo Robot
import sys	#Used for closing the running program
import pygame #Gives access to KEYUP/KEYDOWN events
import picamera
import os, os.path
import numpy as np
import tensorflow as tf
import argparse
import os
import sys

camera=picamera.PiCamera()
charpre='p'
accelerate=0
def create_graph(model_file):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference(images, out_file, labels, model_file, k=5):
    answer = None

    # Creates graph from saved GraphDef.
    create_graph(model_file=args['model'])
    if out_file:
        out_file = open(out_file, 'wb', 1)
    
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        for img in images:
            if not tf.gfile.Exists(img):
                tf.logging.fatal('File does not exist %s', img)
                continue
            image_data = tf.gfile.FastGFile(img, 'rb').read()


            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)
            top_k = predictions.argsort()[-k:][::-1]  # Getting top k predictions
            
            vals = []
            for node_id in top_k:
                human_string = labels[node_id]
                score = predictions[node_id]
                vals.append('%s=%.5f' % (human_string, score))
            rec = "%s\t %s" % (img, ", ".join(vals))
            if out_file:
                out_file.write(rec)
                out_file.write("\n")
            else:
                print(rec)    
    if out_file:
        print("Output stored to a file")
        out_file.close()
    return labels[top_k[0]]

if __name__ == '__main__':
      parser = argparse.ArgumentParser(description='Classify Image(s)')
      parser.add_argument('-li','--list', help='List File having input image paths')
      parser.add_argument('-o','--out', help='Output file for storing the content')
      parser.add_argument('-m','--model', help='model file path (protobuf)', required=True)
      parser.add_argument('-l','--labels', help='labels text file', required=True)
      parser.add_argument('-r','--root', help='path to root directory of input data')
      args = vars(parser.parse_args())
      iteration=0
      while True:
            # Read input
            imagename='/home/pi/Desktop/capture.jpg'
            camera.capture(imagename)
            images = [imagename]
            # if a separate root directory given then make a new path
            if args['root']:
                print("Input data from  : %s" % args['root'])
                images = map(lambda p: os.path.join(args['root'], p), images)

            with open(args['labels'], 'rb') as f:
                labels = [str(w).replace("\n", "") for w in f.readlines()]
            
            
            predictedlabel=run_inference(images=images, out_file=args['out'], labels=labels,        model_file=args['model'])
            
            print(predictedlabel)
            char=predictedlabel 

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
