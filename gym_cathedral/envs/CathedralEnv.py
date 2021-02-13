import math
import hashlib
from operator import add
from enum import IntEnum
import numpy as np

from gym import error, spaces, utils
from gym.utils import seeding

import envs.cathedral as cathedral

TILE_PIXELS = 20

class CathedralEnv(gym.Env):
    
    class Actions(IntEnum):
        # TODO
        place = 0
        
    def __init__(self):
        self.agents = {'white' : 1, 'black' : 2}
        self.mission = {'white': 'win', 'black' : 'win'}
        
        # init vars
        self.game_size  = (10,10,3)
        self.max_steps  = 51
        self.max_squares= 47
        self.step_count = 0
        self.white_pieces, self.black_pieces, self.board = cathedral.setup_game()
        self.window = None
        
          # hider first move
        self.current_agent = 'white'
        self.mission = self.missions[self.current_agent]

        # Action Enumeration
        self.actions = CathedralEnv.Actions
        
        # Observations are dictionaries containing an
        # encoding of the grid and a textual 'mission' string
        self.observation_space = spaces.Box(
            # TODO
            low=0,
            high=2,
            shape=self.game_size,
            dtype='uint8'
        )
        self.observation_space = spaces.Dict({
            'image': self.observation_space
        })
        
        # init the game state
        self.reset()
        
    """
    Compute the reward to be given upon success
    """
    def _reward(self, agent):
        # TODO:: End game reward
        w,b,win = cathedral.score_game(self.white_pieces, self.black_pieces)
        s_reward = 1 - 0.9 * (self.step_count / self.max_steps)
        
        bonus = 0
        if self.current_agent == win:
            bonus = 0.2
        
        if self.current_agent == 'white':
            return 0.8 * (self.white_pieces / self.max_squares) + bonus
        elif self.current_agent == 'black':
            return 0.8 * (self.black_pieces / self.max_squares) + bonus
        
    def _inter_reward(self):
        # TODO:: Determine Intermediate Reward Function
        if self.current_agent == 'hider':
            return ((self.getDistance() - old_dist) / (self.max_steps*10),0)
        elif self.current_agent == 'seeker':
            return (0,(old_dist - self.getDistance()) / (self.max_steps*10))
        
    def get_obs_render(self, obs, tile_size=TILE_PIXELS//2):
        """
        Render an agent observation for visualization
        """
        return self.render()
    
    # TODO
    def step(self, action):
        
        self.step_count += 1
        reward = (0,0)
        done = False
        
        if self.current_agent == 'white':
            self.board, self.white_pieces = cathedral.white_turn(self.board, self.white_pieces)
        elif self.current_agent == 'black':
            self.board, self.black_pieces = cathedral.black_turn(self.board, self.black_pieces)
        
        cathedral.score_game(w,b)
        
            

        # Check if seeker found hider
        if cathedral.game_over(self.board, self.white_pieces, self.black_pieces):
            done = True 
        else:
            reward = self._inter_reward() # TODO::


        # swap current agent
        if self.current_agent == 'hider':
            self.current_agent = 'seeker'
        else:
            self.current_agent = 'hider'

        self.mission = self.missions[self.current_agent]
        obs = self._next_observation()

        #                       , {} = info
        return obs, reward, done, {}
    
    def reset(self):

        self.white_pieces, self.black_pieces, self.board = cathedral.setup_game()
        self.window = None
        
        # white first move
        self.current_agent = 'white'
        
        self.mission = self.missions[self.current_agent]
        self.step_count = 0

        # Return first observation
        return self._next_observation()


    def _next_observation(self):
        tmp = np.zeros(self.game_size)
        tmp[0,0] = self.agents[self.current_agent]
        
        obs = {'board'      : self.board, 
               'agent'    : self.current_agent}
        assert isinstance(obs, dict)
        return obs

    def render(self, mode='human', close=False):
        if close:
            if self.window:
                self.window.close()
            return
        
        # render size
        # WIDTH, HEIGHT = self.game_size[0] * 10, self.game_size[1] * 10

        # img = np.zeros((WIDTH,HEIGHT,3),dtype='uint8')
        tmp = np.zeros((self.game_size))
        for row in self.board:
            for col in row:
                continue # TODO:: color the squares
    
        img = cv2.resize(tmp, (400,400), interpolation=cv2.INTER_NEAREST)

        return img