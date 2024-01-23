import tensorflow as tf
from tensorflow import keras
from keras import models


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image
import os
import csv
import random
import cv2
import glob
# Make NumPy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)


def gen_image(im_1, im_2):

  w, h = 64, 128
  data = np.zeros((h, w), dtype=np.uint8)

  arr_im_1 = np.array(im_1)
  arr_im_2 = np.array(im_2)

  a = 0

  for x in range(len(arr_im_1[0])):
    x = 2*x
    data[x] = arr_im_1[a]
    data[x+1] = arr_im_2[a]
    a = a + 1

  data = data / 255.0

  return data



def print_images(im_1, im_2):
  # Inicjalizacja macierzy 2x3 do przechowywania zdjęć
  rows, cols = 1, 2
  fig, axs = plt.subplots(rows, cols, figsize=(5, 5))


  # Wyświetlenie zdjęcia

  axs[0].imshow(im_1, cmap = 'gray')
  axs[0].axis('off')  # Wyłączenie osi
  axs[0].set_title(f'Zdjęcie 1')

  axs[1].imshow(im_2, cmap = 'gray')
  axs[1].axis('off')  # Wyłączenie osi
  axs[1].set_title(f'Zdjęcie 2')




  
#Zwraca 1 jezeli osoby s podobne, 0 jak sa rozne
def face_recognaction(im_1, im_2, print):

  model = models.Sequential()
  model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy','mse'])

  model = tf.keras.models.load_model('./Model_przeplatane_wiersze.h5', compile=False)


  con = gen_image(im_1, im_2)


  if print:
    print_images(im_1, im_2)

  images_test = []

  images_test.append(con)
  x_test = np.array(images_test)

  predict_x = model.predict(x_test)
  prediction = (predict_x > 0.5).astype("int32")

  pred = [prediction[0][0], predict_x[0][0]]

  return pred