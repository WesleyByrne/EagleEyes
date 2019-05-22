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

# Categories for videos
CATEGORIES = ["Normal", "Anomaly"]
# Resolution to use (ex: 100x100)
FRAME_REZ = 100
# Number of frames in one batch
NUM_FRAMES_IN_BATCH = 100
# Skip factor (ex: if set to 4, then remove first quater of frames from batch,
#   shift everything to the begining and populate created space with new frames)
SKIP_FACTOR = 1.25 # 4

# Load a model we want to use
test_model = tf.keras.models.load_model("new-vgg-test-1epochs-1553182342.model")

# Open a video
cap = cv2.VideoCapture(vid_path)
# Get a number of frames in a video
nframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# We will be ignoring leftover frames
nframe -= nframe % NUM_FRAMES_IN_BATCH
framearray = []

# Only use every 4th frame
for i in range(nframe//4):
   cap.set(cv2.CAP_PROP_POS_FRAMES, i*4)
   ret, frame = cap.read()

   # Resize a frame to proper rezolution
   frame = cv2.resize(frame, (FRAME_REZ, FRAME_REZ))

   # Convert to RGB
   frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   image = img_to_array(frame)

   # Reshape to FRAME_REZxFRAME_REZxCHANNELS
   image = image.reshape((image.shape[0], image.shape[1], image.shape[2]))
   frame = preprocess_input(image)

   # Add to the list
   framearray.append(frame)
   if len(framearray) == NUM_FRAMES_IN_BATCH:
       # Reshape to input format: NUM_BATCHESxNUM_FRAMES_IN_BATCHxFRAME_REZxFRAME_REZxCHANNELS
       framearray = np.array(framearray)
       framearray = framearray.reshape(1, framearray.shape[0], framearray.shape[1], framearray.shape[2], framearray.shape[3])

       # Run prediction on a framearray
       predict = test_model.predict(framearray)
       print("Prediction: ", predict)

       # Remove first 3/4ths and shift eveything back
       framearray = framearray[int(NUM_FRAMES_IN_BATCH/SKIP_FACTOR):]

cap.release()