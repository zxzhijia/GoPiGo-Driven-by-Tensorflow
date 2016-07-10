import socket               # Import socket module
import time
import sys	#Used for closing the running program
import os, os.path
import numpy as np
import tensorflow as tf
import argparse
import os
import sys

charpre='p'
accelerate=0
def create_graph(model_file):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference(images, out_file, labels, model_file, k=2):
    answer = None

    # Creates graph from saved GraphDef.
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
      s = socket.socket()         # Create a socket object
     # host = socket.gethostname() # Get local machine name
      port = 12344                 # Reserve a port for your service.
      s.bind(('', port))        # Bind to the port
      f = open('torecv.jpg','wb')
      create_graph(model_file=args['model'])
      while True:
            # Read input
            f = open('torecv.jpg','wb')
            print('listening')
    	    s.listen(5)                 # Now wait for client connection.
    	    c, addr = s.accept()     # Establish connection with client.
            print 'Got connection from', addr
            print "Receiving..."
            l = c.recv(1024)
	    while (l):
		f.write(l)
		l = c.recv(1024)
	    f.close()
	    print "Done Receiving"
 
            
            imagename='/home/xu/Desktop/torecv.jpg'
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
            
            c.send(char)
	    c.close()                # Close the connection

    

