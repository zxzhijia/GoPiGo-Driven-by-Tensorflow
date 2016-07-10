import numpy as np
import tensorflow as tf
import argparse
import os
import sys

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
    create_graph(model_file)

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
    parser.add_argument('-i','--in', help='Input Image file ')
    parser.add_argument('-li','--list', help='List File having input image paths')
    parser.add_argument('-o','--out', help='Output file for storing the content')
    parser.add_argument('-m','--model', help='model file path (protobuf)', required=True)
    parser.add_argument('-l','--labels', help='labels text file', required=True)
    parser.add_argument('-r','--root', help='path to root directory of input data')
    args = vars(parser.parse_args())
    # Read input
    if not args['in'] and not args['list']:
        print("Either -in or -list option is required.")
        sys.exit(1)
    if args['in']:
        images = [args['in']]
    else:  # list must be given
        with open(args['list']) as ff:
            images = filter(lambda x: x, map(lambda y: y.strip(), ff.readlines()))

    # if a separate root directory given then make a new path
    if args['root']:
        print("Input data from  : %s" % args['root'])
        images = map(lambda p: os.path.join(args['root'], p), images)

    with open(args['labels'], 'rb') as f:
        labels = [str(w).replace("\n", "") for w in f.readlines()]

    predictedlabel=run_inference(images=images, out_file=args['out'], labels=labels, model_file=args['model'])
    print(predictedlabel)

