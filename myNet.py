# -*- coding: utf-8 -*-

""" AlexNet.
Applying 'Alexnet' to Oxford's 17 Category Flower Dataset classification task.
References:
    - Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet
    Classification with Deep Convolutional Neural Networks. NIPS, 2012.
Links:
    - [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
"""

from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
from tflearn.optimizers import SGD

def mynet(height, width, outputs, learning_rate, checkpoint_path, tensorboard_dir):
    # Real-time image preprocessing
    #img_prep = tflearn.ImagePreprocessing()
    # Zero Center (With mean computed over the whole dataset)
    #img_prep.add_featurewise_zero_center()
    # STD Normalization (With std computed over the whole dataset)
    #img_prep.add_featurewise_stdnorm()

    # Data augmentation
    img_aug = tflearn.ImageAugmentation()
    img_aug.add_random_rotation(max_angle=10.0)
    #img_aug.add_random_blur(sigma_max=3.0)
    img_aug.add_random_crop((height, width), 10)

    network = input_data(shape=[None, height, width , 1],name='inputs')#,
                     #data_preprocessing=img_prep,
                     #data_augmentation=img_aug)

    network = conv_2d(network, 96, 11, strides=4, activation='leakyrelu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = conv_2d(network, 256, 5, activation='leakyrelu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = conv_2d(network, 256, 3, activation='leakyrelu')
    network = conv_2d(network, 256, 3, activation='leakyrelu')
    network = conv_2d(network, 256, 3, activation='leakyrelu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = fully_connected(network, 1024, activation='leakyrelu')
    network = dropout(network, 0.5)
    network = fully_connected(network, 512, activation='leakyrelu')
    network = dropout(network, 0.5)
    network = fully_connected(network, outputs, activation='softmax')

    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=learning_rate,
                         name='targets')

    # Training
    model = tflearn.DNN(network, checkpoint_path=checkpoint_path,
                        tensorboard_dir=tensorboard_dir,
                        max_checkpoints=1, tensorboard_verbose=0)
    return model
