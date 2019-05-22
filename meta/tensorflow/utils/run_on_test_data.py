from tensorflow.keras.layers import Dense, Input, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, GlobalAveragePooling2D, CuDNNLSTM, ZeroPadding3D, TimeDistributed
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.utils import Sequence
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img
from tensorflow.keras.optimizers import Nadam

import matplotlib.pyplot as plot
import tensorflow as tf
import numpy as np
import pickle
import random
import ntpath
import time
import cv2
import os

CATEGORIES = ["Normal", "Anomaly"]

test_model = tf.keras.models.load_model("new-vgg-test-1epochs-1553182342.model")
temp = []
for vid in os.listdir("./data/train/"):
   temp.append(os.path.join("./data/train/", vid))

random.shuffle(temp)
for x in temp:
   # Read batches of frames
   tmp_batch = pickle.load(open(x, "rb"))
   fin_batch = []
   cnt = 0

   # For each frame in a batch
   for tmp_frame in tmp_batch:
       # Convert it to float
       tmp_frame = preprocess_input(tmp_frame)
       # Add processed frame to new batch
       fin_batch.append(tmp_frame)
       cnt += 1

       if cnt == 25:
           y = []
           if "Normal" in x:
               ind = CATEGORIES.index("Normal")
               y = [1, 0]
           else:
               ind = CATEGORIES.index("Anomaly")
               y = [0, 1]

           fin_batch = np.array(fin_batch)
           fin_batch = fin_batch.reshape(1, fin_batch.shape[0], fin_batch.shape[1], fin_batch.shape[2], fin_batch.shape[3])

           predict = test_model.predict(fin_batch)
           print("Looking at a {} video, prediction: {}".format(CATEGORIES[ind], predict))

           fin_batch = []
           cnt = 0
