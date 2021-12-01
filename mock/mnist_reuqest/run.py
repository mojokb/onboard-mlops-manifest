import numpy as np
import random
import requests
import time
import os
from os import environ
import cv2

outdir = "/mnist_image"

if environ.get("DOWNLOAD") != 'false':
  test_image = 't10k-images-idx3-ubyte'
  test_label = 't10k-labels-idx1-ubyte'
  
  for f in [test_image, test_label]:
      os.system('wget --no-check-certificate http://yann.lecun.com/exdb/mnist/%s.gz' % (f,))
  
  for f in [test_image, test_label]:
      os.system('gunzip %s.gz' % (f,))
  
  for image_f, label_f in [(test_image, test_label)]:
      with open(image_f, 'rb') as f:
          images = f.read()
      with open(label_f, 'rb') as f:
          labels = f.read()
  
      images = [d for d in images[16:]]
      images = np.array(images, dtype=np.uint8)
      images = images.reshape((-1, 28, 28))
  
  
      if not os.path.exists(outdir):
          os.mkdir(outdir)
      for k, image in enumerate(images):
          cv2.imwrite(os.path.join(outdir, '%05d.png' % (k,)), image)
  
      labels = [outdir + '/%05d.png %d' % (k, l) for k, l in enumerate(labels[8:])]
      with open('%s.txt' % label_f, 'w') as f:
          f.write(os.linesep.join(labels))
  
  
images = [i for i in range(10000)]
random.shuffle(images)

url = os.environ['PREDICT_SERVER_PATH']
sleep_time = os.environ['SLEEP_TIME']

for i in images:
    files = {'media': open(os.path.join(outdir, '%05d.png' % i), 'rb')}
    requests.post(url, files=files)
    time.sleep(float(sleep_time))
