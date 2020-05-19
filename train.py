from glob import glob
import argparse

import torch
from torch import nn, optim
from torch.distributions import Categorical

import copy
import gym
import pyBaba
from tensorboardX import SummaryWriter

from core import environment, options
from core.models.network import Network
import config

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_action(env, net, state):
    state = torch.tensor(state).to(device)
    policy = net(state)

    m = Categorical(policy)
    action = m.sample()

    net.log_probs.append(m.log_prob(action))
    return env.action_space[action.item()]


def train(net, opt):
    R = 0

    loss = []
    returns = []

    for r in net.rewards[::-1]:
        R = r + 0.99 * R
        returns.insert(0, R)

    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + 1e-5)

    for prob, R in zip(net.log_probs, returns):
        loss.append(-prob * R)

    opt.zero_grad()

    loss = torch.cat(loss).sum()
    loss.backward()

    opt.step()

    del net.log_probs[:]
    del net.rewards[:]


def choose_map(map_root):
    import random
    map_list = list(glob(map_root + '/*.txt'))
    return map_list[1]
    # return random.choice(map_list)

def main(args):
    map_path = choose_map(config.MAP_ROOT)
    env = gym.make('baba-is-you-v0', 
                   enable_render=args.enable_render, 
                   map_path=map_path)

    net = Network(H=env.H, W=env.W).to(device)
    opt = optim.Adam(net.parameters(), lr=1e-3)
    writer = SummaryWriter()

    global_step = 0

    for e in range(args.num_episode):
        score = 0
        # state: [batch_size, num_obj_types + 2 (is_text and is_rule), h, w]
        state = env.reset().reshape(1, -1, env.H, env.W)

        step = 0 
        while step < args.num_steps_per_episode:
            text = 'Episode %d, Step %d' % (e, global_step)
            global_step += 1

            action = get_action(env, net, state)

            env.render(text=text)

            next_state, reward, done, _ = env.step(action)
            next_state = next_state.reshape(1, -1, env.H, env.W)

            net.rewards.append(reward)
            score += reward
            state = copy.deepcopy(next_state)

            step += 1
            if env.done:
                env.render(text=text)
                break

        train(net, opt)

        writer.add_scalar('Reward', score, e)
        writer.add_scalar('Step', step, e)

        print(
            f'Episode {e}: score: {score:.3f} time_step: {global_step} step: {step}')


if __name__ == '__main__':
    args = options.get_training_args()
    main(args)

