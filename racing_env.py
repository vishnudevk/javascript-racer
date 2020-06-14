from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts
from game import Game

tf.compat.v1.enable_v2_behavior()


class RaceGameEnv(py_environment.PyEnvironment):

    def __init__(self):
        self.game = Game()
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=4, name='action')


        observation_spec =  {
            'image': array_spec.BoundedArraySpec((16, 16, 3), np.float32, minimum=0,
                                        maximum=255),
            'vector': array_spec.BoundedArraySpec((5,), np.float32, minimum=-100,
                                          maximum=100)}


        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1,), dtype=np.int32, minimum=0, name='observation')
        self._state = 0
        self._episode_ended = False

