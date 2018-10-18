from __future__ import print_function
import numpy as np
import tensorflow as tf
from six.moves import cPickle as pickle
from six.moves import range

PICKLE_FILE = 'emotion_dataset.pickle'     # pickle file in which the preprocessed datasets are stored
MODEL_CKPT = 'checkpoints/my_model'        # checkpoint file
MODEL_NAME = 'emotion_classifier.pb'       # file which contains the frozen graph
EXPORT_DIR = '.'                           # directory which stores the frozen graph files

NUM_CLASSES = 5         # Number of emotion types

IMAGE_HEIGHT = 128      # Height of each input image
IMAGE_WIDTH = 128       # Width of each input image
NUM_CHANNELS = 1        # Number of channels (1 for grayscale images, 3 for RGB images)
BATCH_SIZE = 64         # mini batch size

# Convolutional kernel sizes.
PATCH_SIZE1 = 7
PATCH_SIZE2 = 5
PATCH_SIZE3 = 5
PATCH_SIZE4 = 5

# Convolutional layer depths.
DEPTH1 = 8
DEPTH2 = 8
DEPTH3 = 8
DEPTH4 = 16

# Strides for max-pool layers.
POOL_STRIDE1 = 2
POOL_STRIDE2 = 2
POOL_STRIDE3 = 2

# Number of nodes for fully connected layers.
NUM_HIDDEN1 = 32
NUM_HIDDEN2 = 32
NUM_HIDDEN3 = 16

BETA = 0.009          # regularization

NUM_STEPS = 10001       # number of training steps

# Loading datasets from pickle files.
with open(PICKLE_FILE, 'rb') as f:
    save = pickle.load(f)
    train_dataset = save['train_dataset']
    train_labels = save['train_labels']
    valid_dataset = save['valid_dataset']
    valid_labels = save['valid_labels']
    test_dataset = save['test_dataset']
    test_labels = save['test_labels']
    del save  # hint to help gc free up memory
    print('Training set', train_dataset.shape, train_labels.shape)
    print('Validation set', valid_dataset.shape, valid_labels.shape)
    print('Test set', test_dataset.shape, test_labels.shape)

# Converting data to required format.
def reformat(dataset, labels):
    dataset = dataset.reshape((-1, IMAGE_HEIGHT, IMAGE_WIDTH, NUM_CHANNELS)).astype(np.float32)
    labels = (np.arange(NUM_CLASSES) == labels[:, None]).astype(np.float32)
    return dataset, labels


train_dataset, train_labels = reformat(train_dataset, train_labels)
valid_dataset, valid_labels = reformat(valid_dataset, valid_labels)
test_dataset, test_labels = reformat(test_dataset, test_labels)
print('Training set', train_dataset.shape, train_labels.shape)
print('Validation set', valid_dataset.shape, valid_labels.shape)
print('Test set', test_dataset.shape, test_labels.shape)

# Create some wrappers for simplicity.
def conv2d(x, W, b, strides=1):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)

def maxpool2d(x, stride, k=2):
    return tf.nn.max_pool(x,ksize=[1,k,k,1],strides=[1,stride,stride,1],padding='SAME')

def accuracy(predictions, labels):
    return (100.0 * np.sum(np.argmax(predictions, 1)==np.argmax(labels, 1)) / predictions.shape[0])


# Defining the graph
graph = tf.Graph()
with graph.as_default():
    # Input data.
    tf_train_dataset = tf.placeholder(tf.float32, shape=(BATCH_SIZE, IMAGE_HEIGHT, IMAGE_WIDTH, NUM_CHANNELS))
    tf_train_labels = tf.placeholder(tf.float32, shape=(BATCH_SIZE, NUM_CLASSES))
    tf_valid_dataset = tf.constant(valid_dataset)

    # Variables ( Weights and Biases)
    layer1_weights = tf.get_variable("layer1_weights",
        shape=[PATCH_SIZE1, PATCH_SIZE1,NUM_CHANNELS, DEPTH1],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer1_biases = tf.Variable(tf.zeros([DEPTH1]))

    layer2_weights = tf.get_variable("layer2_weights",
        shape=[PATCH_SIZE2, PATCH_SIZE2, DEPTH1, DEPTH2],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer2_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH2]))

    layer3_weights =tf.get_variable("layer3_weights",
        shape=[PATCH_SIZE3, PATCH_SIZE3, DEPTH2, DEPTH3],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer3_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH3]))

    layer4_weights =tf.get_variable("layer4_weights",
        shape=[PATCH_SIZE4, PATCH_SIZE4, DEPTH3, DEPTH3],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer4_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH3]))

    layer5_weights =tf.get_variable("layer5_weights",
        shape=[PATCH_SIZE4, PATCH_SIZE4, DEPTH3, DEPTH3],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer5_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH3]))

    layer6_weights = tf.get_variable("layer6_weights",
        shape=[IMAGE_HEIGHT//(POOL_STRIDE1*POOL_STRIDE2*POOL_STRIDE3) * IMAGE_WIDTH//(POOL_STRIDE1*POOL_STRIDE2*POOL_STRIDE3) * DEPTH3, NUM_HIDDEN1],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer6_biases = tf.Variable(tf.constant(1.0, shape=[NUM_HIDDEN1]))

    layer7_weights = tf.get_variable("layer7_weights",
        shape=[NUM_HIDDEN1, NUM_HIDDEN2],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer7_biases = tf.Variable(tf.constant(1.0, shape=[NUM_HIDDEN2]))

    layer8_weights = tf.get_variable("layer8_weights",
        shape=[NUM_HIDDEN2, NUM_HIDDEN3],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer8_biases = tf.Variable(tf.constant(1.0, shape=[NUM_HIDDEN3]))

    layer9_weights = tf.get_variable("layer9_weights",
        shape=[NUM_HIDDEN3, NUM_CLASSES],
        initializer=tf.contrib.layers.xavier_initializer()
        )
    layer9_biases = tf.Variable(tf.constant(1.0, shape=[NUM_CLASSES]))


    # Model.
    def model(data):
        conv1 = tf.nn.conv2d(data, layer1_weights, [1, 1, 1, 1], padding='SAME')
        hidden1 = tf.nn.relu(conv1 + layer1_biases)
        hidden1 = maxpool2d(hidden1, POOL_STRIDE1, 3)
        conv2 = tf.nn.conv2d(hidden1, layer2_weights, [1, 1, 1, 1], padding='SAME')
        hidden2 = tf.nn.relu(conv2 + layer2_biases)
        conv3 = tf.nn.conv2d(hidden2, layer3_weights, [1, 1, 1, 1], padding='SAME')
        hidden3 = tf.nn.relu(conv3 + layer3_biases)
        conv4 = tf.nn.conv2d(hidden3, layer4_weights, [1, 1, 1, 1], padding='SAME')
        hidden4 = tf.nn.relu(conv4 + layer4_biases)
        hidden4 = maxpool2d(hidden4, POOL_STRIDE2)
        conv5 = tf.nn.conv2d(hidden4, layer5_weights, [1, 1, 1, 1], padding='SAME')
        hidden5 = tf.nn.relu(conv5 + layer5_biases)
        hidden5 = maxpool2d(hidden5, POOL_STRIDE3, 3)
        shape = hidden5.get_shape().as_list()
        fc = tf.reshape(hidden5, [shape[0], shape[1] * shape[2] * shape[3]])
        fc = tf.nn.relu(tf.matmul(fc, layer6_weights) + layer6_biases)
        fc2 = tf.nn.relu(tf.matmul(fc, layer7_weights) + layer7_biases)
        fc3 = tf.nn.relu(tf.matmul(fc2, layer8_weights) + layer8_biases)
        output = tf.matmul(fc3, layer9_weights) + layer9_biases
        return output


    # Training computation.
    logits = model(tf_train_dataset)
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=tf_train_labels, logits=logits))
    regularizers = (tf.nn.l2_loss(layer1_weights)
        + tf.nn.l2_loss(layer2_weights)
        + tf.nn.l2_loss(layer3_weights)
        + tf.nn.l2_loss(layer4_weights)
        + tf.nn.l2_loss(layer5_weights)
        + tf.nn.l2_loss(layer6_weights)
        + tf.nn.l2_loss(layer7_weights))
    loss=tf.reduce_mean(loss + BETA*regularizers)

    # Count the number of steps taken.
    global_step = tf.Variable(0)

    # Optimizer
    optimizer = tf.train.AdamOptimizer().minimize(loss, global_step=global_step)

    # Predictions
    train_prediction = tf.nn.softmax(logits)
    valid_prediction = tf.nn.softmax(model(tf_valid_dataset))

    # Saver to save the trained model checkpoints
    saver = tf.train.Saver(max_to_keep=8)

# Start training
with tf.Session(graph=graph) as session:
    tf.global_variables_initializer().run()
    print('Initialized')
    for step in range(NUM_STEPS):
        offset = (step * BATCH_SIZE) % (train_labels.shape[0] - BATCH_SIZE)
        batch_data = train_dataset[offset : (offset + BATCH_SIZE), : , : , :]
        batch_labels = train_labels[offset : (offset + BATCH_SIZE), :]
        feed_dict = {tf_train_dataset: batch_data, tf_train_labels: batch_labels}
        _, l, predictions = session.run([optimizer, loss, train_prediction], feed_dict=feed_dict)

        if (step%50 == 0):
            print('Minibatch loss at step %d: %f' % (step, l))
            print('Minibatch accuracy: %.1f%%' % accuracy(predictions, batch_labels))
            v_accuracy=accuracy(valid_prediction.eval(), valid_labels)
            print('Validation accuracy: %.1f%%' % v_accuracy)

            # Save a checkpoint after every 50 steps
            saver.save(session, MODEL_CKPT, global_step=step)

    # Evaluate the tf variables
    WC1 = layer1_weights.eval(session)
    BC1 = layer1_biases.eval(session)
    WC2 = layer2_weights.eval(session)
    BC2 = layer2_biases.eval(session)
    WC3 = layer3_weights.eval(session)
    BC3 = layer3_biases.eval(session)
    WC4 = layer4_weights.eval(session)
    BC4 = layer4_biases.eval(session)
    WC5 = layer5_weights.eval(session)
    BC5 = layer5_biases.eval(session)
    WD1 = layer6_weights.eval(session)
    BD1 = layer6_biases.eval(session)
    WD2 = layer7_weights.eval(session)
    BD2 = layer7_biases.eval(session)
    WD3 = layer8_weights.eval(session)
    BD3 = layer8_biases.eval(session)
    W_OUT = layer9_weights.eval(session)
    B_OUT = layer9_biases.eval(session)

# Defining the frozen graph to be saved
g = tf.Graph()
with g.as_default():
    x_input = tf.placeholder(tf.float32, shape=[None, IMAGE_HEIGHT, IMAGE_WIDTH, NUM_CHANNELS], name="input")

    WC1 = tf.constant(WC1, name="WC1")
    BC1 = tf.constant(BC1, name="BC1")
    CONV1 = conv2d(x_input, WC1, BC1)
    MAXPOOL1 = maxpool2d(CONV1, POOL_STRIDE1, 3)

    WC2 = tf.constant(WC2, name="WC2")
    BC2 = tf.constant(BC2, name="BC2")
    CONV2 = conv2d(MAXPOOL1, WC2, BC2)

    WC3 = tf.constant(WC3, name="WC3")
    BC3 = tf.constant(BC3, name="BC3")
    CONV3 = conv2d(CONV2, WC3, BC3)

    WC4 = tf.constant(WC4, name="WC4")
    BC4 = tf.constant(BC4, name="BC4")
    CONV4 = conv2d(CONV3, WC4, BC4)
    MAXPOOL4 = maxpool2d(CONV4,POOL_STRIDE2)

    WC5 = tf.constant(WC5, name="WC5")
    BC5 = tf.constant(BC5, name="BC5")
    CONV5 = conv2d(MAXPOOL4, WC5, BC5)
    MAXPOOL5 = maxpool2d(CONV5, POOL_STRIDE3, 3)

    WD1 = tf.constant(WD1, name="WD1")
    BD1 = tf.constant(BD1, name="BD1")
    FC1 = tf.reshape(MAXPOOL5, [-1, WD1.get_shape().as_list()[0]])
    FC1 = tf.add(tf.matmul(FC1, WD1), BD1)
    FC1 = tf.nn.relu(FC1)

    WD2 = tf.constant(WD2, name="WD2")
    BD2 = tf.constant(BD2, name="BD2")
    FC2 = tf.add(tf.matmul(FC1, WD2), BD2)
    FC2 = tf.nn.relu(FC2)

    WD3 = tf.constant(WD3, name="WD3")
    BD3 = tf.constant(BD3, name="BD3")
    FC3 = tf.add(tf.matmul(FC2, WD3), BD3)
    FC3 = tf.nn.relu(FC3)

    W_OUT = tf.constant(W_OUT, name="W_OUT")
    B_OUT = tf.constant(B_OUT, name="B_OUT")

    OUTPUT = tf.nn.softmax(tf.matmul(FC3, W_OUT) + B_OUT, name="output")

    sess = tf.Session()
    tf.global_variables_initializer().run(session=sess)

    # Write the frozen graph to the .pb file
    graph_def = g.as_graph_def()
    tf.train.write_graph(graph_def, EXPORT_DIR, MODEL_NAME, as_text=False)
