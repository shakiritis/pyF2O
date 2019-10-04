"""
@author: MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from termcolor import colored


from F2O.utils import data_input_fn

import numpy as np 
import matplotlib.pyplot as plt 


import tensorflow as tf 

class FLAGS:
    TFRECORDS_DIR   = '/home/ansary/RESEARCH/F2O/DataSet/tfrecord/'
    IMAGE_DIM       = 256
    NB_CHANNELS     = 3
    BATCH_SIZE      = 8
    MAKE_ITERATOR   = True

class PARAMS:
    NB_TOTAL_DATA       = 96
    NB_EVAL_DATA        = 16
    N_EPOCHS            = 2
    STEPS_PER_EPOCH     = int( NB_TOTAL_DATA //FLAGS.BATCH_SIZE )
    VALIDATION_STEPS    = int( NB_EVAL_DATA //FLAGS.BATCH_SIZE )

    

#---------------------------------------------------------------------------------------------
train_iterator = data_input_fn(FLAGS,'Train')
eval_iterator  = data_input_fn(FLAGS,'Eval')

#---------------------------------------------------------------------------------------------
def check_data(iterator):
    images,targets=iterator.get_next()
    with tf.Session() as sess:
        x, y = sess.run([images,targets])
        print(x.shape, y.shape)
        for i in range(x.shape[0]):
            plt.imshow(x[i])
            plt.show()
            plt.imshow(y[i])
            plt.show()
            plt.clf()
            plt.close()
        
#--------------------------------------------------------------------------------------------------
def build():
    IN=tf.keras.layers.Input(shape=(FLAGS.IMAGE_DIM,FLAGS.IMAGE_DIM, FLAGS.NB_CHANNELS))
    x = tf.keras.layers.Conv2D(64,(3,3), padding='same',strides=(1,1))(IN)
    x = tf.keras.layers.Conv2D(3,(3,3), padding='same',strides=(1,1))(x)
    return tf.keras.models.Model(inputs=IN,outputs=x)

def tarin_debug(PARAMS):
    model = build()
    model.summary()
    model.compile(
        optimizer=tf.train.AdamOptimizer(),
        loss=tf.keras.losses.mean_absolute_error,
    )

    model.fit(
        train_iterator,
        epochs=PARAMS.N_EPOCHS,
        steps_per_epoch=PARAMS.STEPS_PER_EPOCH,
        validation_data=eval_iterator,
        validation_steps=PARAMS.VALIDATION_STEPS
    )

check_data(train_iterator)
check_data(eval_iterator)
tarin_debug(PARAMS)