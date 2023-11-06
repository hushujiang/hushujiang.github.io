import os

import gym
from agit import Agent#之前的是eternatus
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


def main():
    from datetime import datetime
    start_time = datetime.utcnow()

    print('Python start time: {} UTC'.format(start_time))

    import tensorflow as tf
    print('TensorFlow CUDA is available: {}'.format(tf.config.list_physical_devices('GPU')))

    import torch
    print('pyTorch CUDA is available: {}'.format(torch.cuda.is_available()))

    if 'CLOUD_PROVIDER' in os.environ and os.environ['CLOUD_PROVIDER'] == 'Agit':
        provider = 'Agit'

        log_dir = '/root/.agit'
        results_dir = '/root/.agit'
    else:
        provider = 'local'

        log_dir = '../temp'
        results_dir = '../temp'

    # Initialize Ray Cluster
    #ray_init()

    tune.run(
        'PPO',
        queue_trials=True,  # Don't use this parameter unless you know what you do.
        stop={'training_iteration': 10},
        config={
            'env': SimpleCorridor,
            'env_config': {'corridor_length': 5}
        }
    )

    with open(os.path.join(results_dir, 'model.pkl'), 'wb') as file:
        file.write(b'model data')

    complete_time = datetime.utcnow()

    print('Python complete time: {} UTC'.format(complete_time))

    print('Python resource time: {} UTC'.format(complete_time - start_time))


if __name__ == '__main__':
    main()