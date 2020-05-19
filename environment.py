import gym
from gym.utils import seeding
from gym.envs.registration import register
import numpy as np
import config
import pyBaba
import rendering


class BabaEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, map_path="baba-is-auto/Resources/Maps/baba_is_you.txt", 
                 enable_render=True):
        super(BabaEnv, self).__init__()

        self.path = map_path
        _map = open(self.path)
        self.W, self.H =[int(x) for x in  _map.readline().strip().split()]
        self.ids = np.array([l.strip().split() for l in _map ])
        _map.close()

        self.game = pyBaba.Game(self.path)
        self.renderer = rendering.Renderer(self.game, enable_render=enable_render)

        self.action_space = [
            pyBaba.Direction.UP,
            pyBaba.Direction.DOWN,
            pyBaba.Direction.LEFT,
            pyBaba.Direction.RIGHT
        ]

        self.action_size = len(self.action_space)

        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)

        return [seed]

    def reset(self):
        self.game.Reset()
        self.done = False
        return self.get_obs()

    def step(self, action):
        self.game.MovePlayer(action)

        result = self.game.GetPlayState()

        if result == pyBaba.PlayState.LOST:
            self.done = True
            reward = -500
        elif result == pyBaba.PlayState.WON:
            self.done = True
            reward = 200
        else:
            reward = -0.5

        return self.get_obs(), reward, self.done, {}

    def render(self, mode='human', close=False, text=""):
        if close:
            self.renderer.quit_game()

        return self.renderer.render(self.game.GetMap(), mode, text=text)

    def get_obs(self):
        return np.array(
            pyBaba.Preprocess.StateToTensor(self.game),
            dtype=np.float32).reshape(-1, self.game.GetMap().GetHeight(), self.game.GetMap().GetWidth())


register(
    id='baba-outofreach-v0',
    entry_point='environment:BabaEnv',
    max_episode_steps=200,
    nondeterministic=True,
    kwargs={
        'enable_render': True, 
        'map_path': 'baba-is-auto/Resources/Maps/out_of_reach.txt',
    },
)
