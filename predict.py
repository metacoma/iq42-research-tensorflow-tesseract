#!/usr/bin/python3
# coding=utf-8
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
import model
import datetime
import time
from icdar import restore_rectangle
import lanms
import os
from eval import resize_image, sort_poly, detect
import collections
import json
from PIL import Image
import pytesseract
import cv2

def text_detection(img_path):
  start_time = time.time()
  rtparams = collections.OrderedDict()

  img = cv2.imread(img_path, 1)
  im_resized, (ratio_h, ratio_w) = resize_image(img)

  rtparams['start_time'] = datetime.datetime.now().isoformat()
  rtparams['image_size'] = '{}x{}'.format(img.shape[1], img.shape[0])



  rtparams['working_size'] = '{}x{}'.format(
    im_resized.shape[1], im_resized.shape[0])

  timer = collections.OrderedDict([
    ('net', 0),
    ('restore', 0),
    ('nms', 0)
  ])

  start = time.time()
  score, geometry = sess.run(
    [f_score, f_geometry],
    feed_dict={input_images: [im_resized[:,:,::-1]]})
  timer['net'] = time.time() - start
  boxes, timer = detect(score_map=score, geo_map=geometry, timer=timer)

  print('net {:.0f}ms, restore {:.0f}ms, nms {:.0f}ms'.format(
    timer['net']*1000, timer['restore']*1000, timer['nms']*1000))

  if boxes is not None:
      scores = boxes[:,8].reshape(-1)
      boxes = boxes[:, :8].reshape((-1, 4, 2))
      boxes[:, :, 0] /= ratio_w
      boxes[:, :, 1] /= ratio_h

  duration = time.time() - start_time
  timer['overall'] = duration
  print('[timing] {}'.format(duration))

  if boxes is not None:
      text_lines = []
      for box, score in zip(boxes, scores):
          box = sort_poly(box.astype(np.int32))
          if np.linalg.norm(box[0] - box[1]) < 5 or np.linalg.norm(box[3]-box[0]) < 5:
              continue
          tl = collections.OrderedDict(zip(
              ['x0', 'y0', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3'],
              map(float, box.flatten())))
          tl['score'] = float(score)
          text_lines.append(tl)

  #print(text_lines)
  return text_lines

def tesseract(src_image, x, y, width, height):
  image = src_image[y:y+height, x:x+width]
  try:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  except:
    print("------------- ERROR --------------")
    return
  gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

  filename = "{}.png".format(os.getpid())
  cv2.imwrite(filename, gray)
  cv2.imwrite(filename, image)

  text = pytesseract.image_to_string(Image.open(filename), "eng+rus")
  os.remove(filename)
  return text


checkpoint_path = './east_icdar2015_resnet_v1_50_rbox'

input_images = tf.placeholder(tf.float32, shape=[None, None, None, 3], name='input_images')
global_step = tf.get_variable('global_step', [], initializer=tf.constant_initializer(0), trainable=False)
f_score, f_geometry = model.model(input_images, is_training=False)

variable_averages = tf.train.ExponentialMovingAverage(0.997, global_step)
saver = tf.train.Saver(variable_averages.variables_to_restore())
sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
ckpt_state = tf.train.get_checkpoint_state(checkpoint_path)

model_path = os.path.join(checkpoint_path, os.path.basename(ckpt_state.model_checkpoint_path))
saver.restore(sess, model_path)

#text_detection("/tmp/azure-subscription.png");

image_path = "/tmp/telega.png"

boxes = text_detection(image_path)
print(json.dumps(boxes, indent=4))
original_image = cv2.imread(image_path)

advanced_boxes = []

THRESHOLD_X=10
THRESHOLD_Y=10

i = 0
j = 0
for box in boxes:
    match = False
    for advanced_box in advanced_boxes:
      if abs(box["y0"] - advanced_box["y0"]) < THRESHOLD_Y:
        if (advanced_box["x0"] + (advanced_box["x2"] - advanced_box["x0"]) - box["x0"] < THRESHOLD_X):
          advanced_box["x2"] = box["x2"]
          advanced_box["y2"] = box["y2"]
          match = True
          break;
        if (box["x0"] + (box["x2"] - box["x0"]) - advanced_box["x0"] < THRESHOLD_X):
          advanced_box["x0"] = box["x0"]
          advanced_box["y2"] = box["y2"]
          match = True
          break;

    if not match:
      j = j + 1
      print("#{} add box".format(j))
      advanced_boxes.append(box)

print("Boxes count: {}, advanced boxes count: {}".format(len(boxes), len(advanced_boxes)))

i = 0
for box in advanced_boxes:
    print("{4},convert ~/Downloads/bpm.png -crop {0}x{1}+{2}+{3} - | display".format(int(box["x2"] - box["x0"]), int(box["y2"] - box["y0"]), int(box["x0"]), int(box["y0"]), i))
    i = i + 1
    box["x0"] = box["x0"] - 6
    box["y0"] = box["y0"] - 5

    box["x2"] = box["x2"] + 6
    box["y2"] = box["y2"] + 5

    print(tesseract(original_image, int(box["x0"]), int(box["y0"]), int(box["x2"] - box["x0"]), int(box["y2"] - box["y0"])))
