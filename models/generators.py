"""
@author: MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from termcolor import colored

import os
import numpy as np 
import matplotlib.pyplot as plt

import tensorflow as tf 

#---------------------------------UNET From Official Tensorflow pix2pix----------------------------------------
def downsample(filters, size, apply_batchnorm=True):
    initializer = tf.random_normal_initializer(0., 0.02)
    result = tf.keras.Sequential()
    result.add(tf.keras.layers.Conv2D(filters, size, strides=2, padding='same',kernel_initializer=initializer, use_bias=False))
    if apply_batchnorm:
        result.add(tf.keras.layers.BatchNormalization())
    result.add(tf.keras.layers.LeakyReLU())
    return result
def upsample(filters, size, apply_dropout=False):
    initializer = tf.random_normal_initializer(0., 0.02)
    result = tf.keras.Sequential()
    result.add(tf.keras.layers.Conv2DTranspose(filters, size, strides=2,padding='same',kernel_initializer=initializer,use_bias=False))
    result.add(tf.keras.layers.BatchNormalization())
    if apply_dropout:
        result.add(tf.keras.layers.Dropout(0.5))
    result.add(tf.keras.layers.ReLU())
    return result
def UNET():
    down_stack = [  downsample(64, 4, apply_batchnorm=False), # (bs, 128, 128, 64)
                    downsample(128, 4), # (bs, 64, 64, 128)
                    downsample(256, 4), # (bs, 32, 32, 256)
                    downsample(512, 4), # (bs, 16, 16, 512)
                    downsample(512, 4), # (bs, 8, 8, 512)
                    downsample(512, 4), # (bs, 4, 4, 512)
                    downsample(512, 4), # (bs, 2, 2, 512)
                    downsample(512, 4), # (bs, 1, 1, 512)
    ]

    up_stack = [    upsample(512, 4, apply_dropout=True), # (bs, 2, 2, 1024)
                    upsample(512, 4, apply_dropout=True), # (bs, 4, 4, 1024)
                    upsample(512, 4, apply_dropout=True), # (bs, 8, 8, 1024)
                    upsample(512, 4), # (bs, 16, 16, 1024)
                    upsample(256, 4), # (bs, 32, 32, 512)
                    upsample(128, 4), # (bs, 64, 64, 256)
                    upsample(64, 4), # (bs, 128, 128, 128)
    ]

    initializer = tf.random_normal_initializer(0., 0.02)
    last = tf.keras.layers.Conv2DTranspose(3, 4,strides=2,padding='same',kernel_initializer=initializer,activation='tanh') # (bs, 256, 256, 3)
    concat = tf.keras.layers.Concatenate()
    inputs = tf.keras.layers.Input(shape=[None,None,3])
    x = inputs

    # Downsampling through the model
    skips = []
    for down in down_stack:
        x = down(x)
        skips.append(x)
    skips = reversed(skips[:-1])
    # Upsampling and establishing the skip connections
    for up, skip in zip(up_stack, skips):
        x = up(x)
        x = concat([x, skip])

    x = last(x)

    return tf.keras.Model(inputs=inputs, outputs=x)
#---------------------------------UNET From Official Tensorflow pix2pix----------------------------------------
