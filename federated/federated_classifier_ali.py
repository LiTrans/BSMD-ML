# Copyright 2018 coMind. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# https://comind.org/
# ==============================================================================

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

#CNN mode detection
from Mode_Detection_CNN import *

# Custom federated hook
from hook import _FederatedHook

# Helper libraries
import os
import numpy as np
from time import time
import matplotlib.pyplot as plt

# Import custom optimizer
import federated_averaging_optimizer

flags = tf.app.flags

flags.DEFINE_boolean("is_chief", False, "True if this worker is chief")
flags.DEFINE_string("worker_name", None, "worker name: worker1, worker2, worker3, worker4")

# Disable GPU for all workers in local testing.
# Enable it when testing in different computers
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# You can safely tune these variables
BATCH_SIZE = 32
EPOCHS = 5
INTERVAL_STEPS = 100 # Steps between averages
WAIT_TIME = 5 # How many seconds to wait for new workers to connect
# -----------------

# Set these IPs to your own, can leave as localhost for local testing
CHIEF_PUBLIC_IP = 'localhost:7777' # Public IP of the chief worker
CHIEF_PRIVATE_IP = 'localhost:7777' # Private IP of the chief worker

# Create the custom hook
FLAGS = flags.FLAGS
federated_hook = _FederatedHook(FLAGS.is_chief, FLAGS.worker_name, CHIEF_PRIVATE_IP, CHIEF_PUBLIC_IP, WAIT_TIME, INTERVAL_STEPS,)

# parameters definition
num_channels_ensemble = [5]
num_filters_ensemble = []
filters_size_ensemble = []
num_stride_maxpool_ensemble = []
num_stride_conv2d_ensemble = []
maxpool_size_ensemble = []

# The data structures in the following data files are different from those in ensemble paper
X_train = np.load("D:/OneDrive - Concordia University - Canada/PycharmProjects/Itinerum-Deep-Neural-Network/data"
                  "/augmenteddata_5channels/X_train_final.npy")

Y_train = np.load("D:/OneDrive - Concordia University - Canada/PycharmProjects/Itinerum-Deep-Neural-Network/data/"
                  "augmenteddata_5channels/Y_train_final.npy")

# I believe we need to split the data, one piece for each worker
# I don't know if this is the proper way for splitting the data
X_train = np.array_split(X_train, federated_hook.num_workers)[federated_hook.task_index]
Y_train = np.array_split(Y_train, federated_hook.num_workers)[federated_hook.task_index]

# You can safely tune this variable
SHUFFLE_SIZE = X_train.shape[0]

# print(Y_train.shape)
Y_onehot = np.zeros((Y_train.shape[0], 4))
Y_onehot[np.arange(Y_train.shape[0]), Y_train] = 1
Y_train = np.copy(Y_onehot)
# print(Y_train.shape)
print('Data loaded')

CHECKPOINT_DIR = 'logs_dir/{}'.format(time())

global_step = tf.train.get_or_create_global_step()

# Define input pipeline, place these ops in the cpu
with tf.name_scope('dataset'), tf.device('/cpu:0'):
    # Placeholders for the iterator
    X_placeholder = tf.placeholder(tf.float32, shape=(None, seg_size, num_channels), name='X_placeholder')
    Y_placeholder = tf.placeholder(tf.float32, shape=[None, num_classes], name='Y_placeholder')
    minibatch_weights = tf.placeholder(tf.float32, shape=[None], name='minibatch_weights')
    batch_size = tf.placeholder(tf.int64, name='batch_size')
    shuffle_size = tf.placeholder(tf.int64, name='shuffle_size')

    # Create data set from numpy arrays, shuffle, repeat and batch
    dataset = tf.data.Dataset.from_tensor_slices((X_placeholder, Y_placeholder))
    dataset = dataset.shuffle(shuffle_size, reshuffle_each_iteration=True)
    dataset = dataset.repeat(EPOCHS)
    dataset = dataset.batch(batch_size)

    iterator = tf.data.Iterator.from_structure(dataset.output_types, dataset.output_shapes)
    dataset_init_op = iterator.make_initializer(dataset, name='dataset_init')
    X, y = iterator.get_next()

# Define our model
num_layers_ensemble, filters_size_ensemble, num_filters_ensemble, maxpool_size_ensemble, num_stride_conv2d_ensemble, \
num_stride_maxpool_ensemble, weights_ensemble = parameters_weights()

filters_size = filters_size_ensemble[0]
num_filters = num_filters_ensemble[0]
num_stride_conv2d = num_stride_conv2d_ensemble[0]
num_stride_maxpool = num_stride_maxpool_ensemble[0]
maxpool_size = maxpool_size_ensemble[0]
weights = weights_ensemble[0]

# Initialize parameters
parameters = initialize_parameters(weights)

# Forward propagation: Build the forward propagation in the tensorflow graph
predictions = forward_propagation(X, parameters, num_stride_conv2d, maxpool_size, num_stride_maxpool)

# Object to keep moving averages of our metrics (for tensorboard)
summary_averages = tf.train.ExponentialMovingAverage(0.9)

# Define cross_entropy loss
with tf.name_scope('loss'):
    # loss = tf.losses.softmax_cross_entropy(onehot_labels=y, logits=predictions, weights=minibatch_weights)
    print("type logits:", type(predictions))
    print("dim logits:", predictions.shape)

    print("type labels:", type(y))
    print("dim labels:", y.shape)
    # loss = tf.reduce_mean(keras.losses.sparse_categorical_crossentropy(y, predictions))
    # loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=predictions)
    loss = tf.losses.softmax_cross_entropy(onehot_labels=y, logits=predictions, weights=1)
    loss_averages_op = summary_averages.apply([loss])
    # Store moving average of the loss
    tf.summary.scalar('cross_entropy', summary_averages.average(loss))

# Define accuracy metric
with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        # Compare prediction with actual label
        correct_prediction = tf.equal(tf.argmax(predictions, 1), tf.cast(tf.argmax(y, 1), tf.int64))
    # Average correct predictions in the current batch
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy_metric')
    accuracy_averages_op = summary_averages.apply([accuracy])
    # Store moving average of the accuracy
    tf.summary.scalar('accuracy', summary_averages.average(accuracy))

with tf.name_scope('train'):
    # Make train_op dependent on moving averages ops. Otherwise they will be
    # disconnected from the graph
    with tf.control_dependencies([loss_averages_op, accuracy_averages_op]):
        train_op = tf.train.AdamOptimizer(0.001).minimize(loss, global_step=global_step)

SESS_CONFIG = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)

N_BATCHES = int(X_train.shape[0] / BATCH_SIZE)
LAST_STEP = int(N_BATCHES * EPOCHS)

SESS_CONFIG = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)


# Logger hook to keep track of the training
class _LoggerHook(tf.train.SessionRunHook):
    def begin(self):
        """ Run this in session begin """
        self._total_loss = 0
        self._total_acc = 0

    def before_run(self, run_context):
        """ Run this in session before_run """
        return tf.train.SessionRunArgs([loss, accuracy, global_step])

    def after_run(self, run_context, run_values):
        """ Run this in session after_run """
        loss_value, acc_value, step_value = run_values.results
        self._total_loss += loss_value
        self._total_acc += acc_value
        if (step_value + 1) % N_BATCHES == 0:
            print("Epoch {}/{} - loss: {:.4f} - acc: {:.4f}".format(
                int(step_value / N_BATCHES) + 1,
                EPOCHS, self._total_loss / N_BATCHES,
                self._total_acc / N_BATCHES))
            self._total_loss = 0
            self._total_acc = 0


class _InitHook(tf.train.SessionRunHook):
    """ Hook to initialize the dataset """
    def after_create_session(self, session, coord):
        """ Run this after creating session """
        session.run(dataset_init_op, feed_dict={
            X_placeholder: X_train,
            Y_placeholder: Y_train,
            batch_size: BATCH_SIZE,
            shuffle_size: SHUFFLE_SIZE})














# Load dataset as numpy arrays
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# Split dataset
train_images = np.array_split(train_images, federated_hook.num_workers)[federated_hook.task_index]
train_labels = np.array_split(train_labels, federated_hook.num_workers)[federated_hook.task_index]

# You can safely tune this variable
SHUFFLE_SIZE = train_images.shape[0]
# -----------------

print('Local dataset size: {}'.format(train_images.shape[0]))

# Normalize dataset
train_images = train_images / 255.0
test_images = test_images / 255.0

CHECKPOINT_DIR = 'logs_dir/{}'.format(time())

global_step = tf.train.get_or_create_global_step()

# Define input pipeline, place these ops in the cpu
with tf.name_scope('dataset'), tf.device('/cpu:0'):
    # Placeholders for the iterator
    images_placeholder = tf.placeholder(train_images.dtype, [None, train_images.shape[1], train_images.shape[2]])
    labels_placeholder = tf.placeholder(train_labels.dtype, [None])
    batch_size = tf.placeholder(tf.int64)
    shuffle_size = tf.placeholder(tf.int64, name='shuffle_size')

    # Create dataset, shuffle, repeat and batch
    dataset = tf.data.Dataset.from_tensor_slices((images_placeholder, labels_placeholder))
    dataset = dataset.shuffle(shuffle_size, reshuffle_each_iteration=True)
    dataset = dataset.repeat(EPOCHS)
    dataset = dataset.batch(batch_size)

    iterator = tf.data.Iterator.from_structure(dataset.output_types, dataset.output_shapes)
    dataset_init_op = iterator.make_initializer(dataset, name='dataset_init')
    X, y = iterator.get_next()

# Define our model
flatten_layer = tf.layers.flatten(X, name='flatten')

dense_layer = tf.layers.dense(flatten_layer, 128, activation=tf.nn.relu, name='relu')

predictions = tf.layers.dense(dense_layer, 10, activation=tf.nn.softmax, name='softmax')

# Object to keep moving averages of our metrics (for tensorboard)
summary_averages = tf.train.ExponentialMovingAverage(0.9)

# Define cross_entropy loss
with tf.name_scope('loss'):
    loss = tf.reduce_mean(keras.losses.sparse_categorical_crossentropy(y, predictions))
    loss_averages_op = summary_averages.apply([loss])
    # Store moving average of the loss
    tf.summary.scalar('cross_entropy', summary_averages.average(loss))

with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        # Compare prediction with actual label
        correct_prediction = tf.equal(tf.argmax(predictions, 1), tf.cast(y, tf.int64))
    # Average correct predictions in the current batch
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    accuracy_averages_op = summary_averages.apply([accuracy])
    # Store moving average of the accuracy
    tf.summary.scalar('accuracy', summary_averages.average(accuracy))

# Define optimizer and training op
with tf.name_scope('train'):
    # Make train_op dependent on moving averages ops. Otherwise they will be
    # disconnected from the graph
    with tf.control_dependencies([loss_averages_op, accuracy_averages_op]):
        train_op = tf.train.AdamOptimizer(0.001).minimize(loss, global_step=global_step)

SESS_CONFIG = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)

N_BATCHES = int(train_images.shape[0] / BATCH_SIZE)
LAST_STEP = int(N_BATCHES * EPOCHS)

# Logger hook to keep track of the training
class _LoggerHook(tf.train.SessionRunHook):
    def begin(self):
        """ Run this in session begin """
        self._total_loss = 0
        self._total_acc = 0

    def before_run(self, run_context):
        """ Run this in session before_run """
        return tf.train.SessionRunArgs([loss, accuracy, global_step])

    def after_run(self, run_context, run_values):
        """ Run this in session after_run """
        loss_value, acc_value, step_value = run_values.results
        self._total_loss += loss_value
        self._total_acc += acc_value
        if (step_value + 1) % N_BATCHES == 0:
            print("Epoch {}/{} - loss: {:.4f} - acc: {:.4f}".format(
                int(step_value / N_BATCHES) + 1,
                EPOCHS, self._total_loss / N_BATCHES,
                self._total_acc / N_BATCHES))
            self._total_loss = 0
            self._total_acc = 0

class _InitHook(tf.train.SessionRunHook):
    """ Hook to initialize the dataset """
    def after_create_session(self, session, coord):
        """ Run this after creating session """
        session.run(dataset_init_op, feed_dict={
            images_placeholder: train_images,
            labels_placeholder: train_labels,
            shuffle_size: SHUFFLE_SIZE, batch_size: BATCH_SIZE})

print("Worker {} ready".format(federated_hook.task_index))

with tf.name_scope('monitored_session'):
    with tf.train.MonitoredTrainingSession(
            checkpoint_dir=CHECKPOINT_DIR,
            hooks=[_LoggerHook(), _InitHook(), federated_hook],
            config=SESS_CONFIG,
            save_checkpoint_steps=N_BATCHES) as mon_sess:
        while not mon_sess.should_stop():
            mon_sess.run(train_op)

print('--- Begin Evaluation ---')
with tf.Session() as sess:
    ckpt = tf.train.get_checkpoint_state(CHECKPOINT_DIR)
    tf.train.Saver().restore(sess, ckpt.model_checkpoint_path)
    print('Model restored')
    sess.run(dataset_init_op, feed_dict={
        images_placeholder: test_images,
        labels_placeholder: test_labels,
        shuffle_size: 1, batch_size: test_images.shape[0]})
    print('Test accuracy: {:4f}'.format(sess.run(accuracy)))