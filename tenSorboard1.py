# The following switch allows the program runs locally and in the Agit environment without modifications.
import os

path = os.path.dirname(__file__)
print(path)

if 'CLOUD_PROVIDER' in os.environ and os.environ['CLOUD_PROVIDER'] == 'Agit':
    logdir = '/root/.agit'   
else:
    logdir = './runs'	
# setup tensorboard path
import tensorflow as tf
writer = tf.summary.create_file_writer(logdir)

''' alternative tensorboards

# pytorch tensorboard :
 from torch.utils.tensorboard import SummaryWriter
 writer = SummaryWriter(log_dir=logdir)

# tensorboardX :
from tensorboardX import SummaryWriter
writer = SummaryWriter(logdir=logdir)

'''

import numpy as np
import time

# a 5 minutes running example, the realtime tensorboard can be viewed in the training page
with writer.as_default():
    for n_iter in range(360):
        tf.summary.scalar('Loss/train', np.random.random(), n_iter)
        tf.summary.scalar('Loss/test', np.random.random(), n_iter)
        tf.summary.scalar('Accuracy/train', np.random.random(), n_iter)
        tf.summary.scalar('Accuracy/test', np.random.random(), n_iter)
        time.sleep(1)