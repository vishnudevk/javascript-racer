from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
import numpy as np
import queue

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

        self._observation_spec = array_spec.BoundedArraySpec((55, 240, 3), dtype=np.float64, minimum=0,
                                        maximum=1,name='observation')
        self._state = self.game.takess()
        self._episode_ended = False
        self._past_speed_queue = queue.Queue(20)
        print("INIT IS TRIGGERED")

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self.game.resetGame()
        self._state = self.game.takess()
        self._episode_ended = False
        self._past_speed_queue = queue.Queue(20)
        print("RESET METHOD IS TRIGGERED")
        #print(self._state.shape)
        return ts.restart(self._state)

    def _step(self, action):

        if self._episode_ended:
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()

        # Make sure episodes don't go on forever.
        if action == 0:
            self.game.move('up')
        elif action == 1:
            self.game.move('left')
        elif action == 2:
            self.game.move('down')
        elif action == 3:
            self.game.move('right')
        elif action == 4:
            self.game.move('none')
        
        #print("STEP METHOD IS TRIGGERED " , action)
        self._state = self.game.takess()
        speed = int(self.game.getSpead())
        
        if(self._past_speed_queue.full()):
            self._past_speed_queue.get()
        self._past_speed_queue.put(speed)
        temp_list = list(self._past_speed_queue.queue)

        #print(temp_list)
        if(len(temp_list)>=20 and max(temp_list)<26):
            print("GAME OVER")
            self._episode_ended = True
            return ts.termination(self._state, reward=-200)
        elif (len(temp_list)>=20):
            speed = speed + int(sum(temp_list)/200) #Additional reward for better average speeds

        
        return ts.transition(self._state, reward=speed, discount=1.0)
        