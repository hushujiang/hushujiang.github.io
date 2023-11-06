import os
#测试单个gpu，没有worker的资源脚本
import gym
import ray
from gym.spaces import Discrete, Box
from ray import tune


class SimpleCorridor(gym.Env):
    def __init__(self, config):
        self.end_pos = config['corridor_length']
        self.cur_pos = 0
        self.action_space = Discrete(2)
        self.observation_space = Box(0.0, self.end_pos, shape=(1,))

    def reset(self):
        self.cur_pos = 0
        return [self.cur_pos]

    def step(self, action):
        if action == 0 and self.cur_pos > 0:
            self.cur_pos -= 1
        elif action == 1:
            self.cur_pos += 1
        done = self.cur_pos >= self.end_pos
        return [self.cur_pos], 1 if done else 0, done, {}


if __name__ == '__main__':
    from datetime import datetime

    start_time = datetime.utcnow()

    print('Python start time: {} UTC'.format(start_time))

    if 'CLOUD_PROVIDER' in os.environ and os.environ['CLOUD_PROVIDER'] == 'Agit':
        from agit import ray_init

        ray_init()
    else:
        ray.init()

    print('Ray Cluster Resources: {}'.format(ray.cluster_resources()))

    import tensorflow as tf

    print('TensorFlow CUDA is available: {}'.format(tf.config.list_physical_devices('GPU')))

    import torch

    print('pyTorch CUDA is available: {}'.format(torch.cuda.is_available()))

    tune.run(
        'PPO',
        queue_trials=True,  # Don't use this parameter unless you know what you do.
        stop={'training_iteration': 10},
        config={
            'env': SimpleCorridor,
            'env_config': {'corridor_length': 5},
            'num_gpus': 1
        }
    )

    complete_time = datetime.utcnow()

    print('Python complete time: {} UTC'.format(complete_time))

    print('Python resource time: {} UTC'.format(complete_time - start_time))