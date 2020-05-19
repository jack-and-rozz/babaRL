import torch
from torch import nn, optim
import torch.nn.functional as F

# From REINFORCE.py
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

# From DQN.py
# class Network(nn.Module):
#     def __init__(self):
#         super(Network, self).__init__()

#         self.conv1 = nn.Conv2d(pyBaba.Preprocess.TENSOR_DIM,
#                                64, 3, padding=1, bias=False)
#         self.bn1 = nn.BatchNorm2d(64)
#         self.conv2 = nn.Conv2d(64, 64, 3, padding=1, bias=False)
#         self.bn2 = nn.BatchNorm2d(64)
#         self.conv3 = nn.Conv2d(64, 64, 3, padding=1, bias=False)
#         self.bn3 = nn.BatchNorm2d(64)
#         self.conv4 = nn.Conv2d(64, 1, 1, padding=0, bias=False)
#         self.bn4 = nn.BatchNorm2d(1)

#         self.fc = nn.Linear(352, 4)

#     def forward(self, x):
#         x = F.relu(self.bn1(self.conv1(x)))
#         x = F.relu(self.bn2(self.conv2(x)))
#         x = F.relu(self.bn3(self.conv3(x)))
#         x = F.relu(self.bn4(self.conv4(x)))

#         x = x.view(x.data.size(0), -1)
#         return self.fc(x)
