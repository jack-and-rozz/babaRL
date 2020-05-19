import argparse
import torch
from torch import nn, optim
import torch.nn.functional as F
from torch.distributions import Categorical

import copy

import gym
import environment
import pyBaba

from tensorboardX import SummaryWriter

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Network(nn.Module):
    def __init__(self, H, W):
        super(Network, self).__init__()
        self.conv1 = nn.Conv2d(pyBaba.Preprocess.TENSOR_DIM, 128, 3, padding=1)
        self.conv2 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv3 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv4 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv5 = nn.Conv2d(128, 1, 1, padding=0)
        # TODO: fix the number of dimensions without depending on the screen size, x*y.
        self.fc = nn.Linear(H * W, 4)

        self.log_probs = []
        self.rewards = []

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = x.view(x.data.size(0), -1)
        x = self.fc(x)
        return F.softmax(x, dim=1)



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


def main(args):

    env = gym.make('baba-outofreach-v0', enable_render=args.enable_render)
    net = Network(H=env.H, W=env.W).to(device)
    opt = optim.Adam(net.parameters(), lr=1e-3)
    writer = SummaryWriter()


    global_step = 0

    for e in range(10000):
        score = 0

        # state: [batch_size, num_obj_types + 2 (is_text and is_rule), h, w]
        state = env.reset().reshape(1, -1, env.H, env.W)
        # state = env.reset().reshape(1, -1, 16, 22)

        step = 0
        while step < 200:
            global_step += 1

            action = get_action(env, net, state)

            env.render()

            next_state, reward, done, _ = env.step(action)
            next_state = next_state.reshape(1, -1, env.H, env.W)

            net.rewards.append(reward)
            score += reward
            state = copy.deepcopy(next_state)

            step += 1

            if env.done:
                env.render()
                break

        train(net, opt)

        writer.add_scalar('Reward', score, e)
        writer.add_scalar('Step', step, e)

        print(
            f'Episode {e}: score: {score:.3f} time_step: {global_step} step: {step}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser( 
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--enable-render', action='store_true', help='If true, the board during training or testing is displayed.')
    args = parser.parse_args()
    main(args)

