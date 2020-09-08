(Part of the codes in this repository can be still incomplete.)

## Overview
This is a repository for training Baba-Is-You agents by RL, for visualizing the agents, and for debugging the simulator.

The simulator can be downloaded from https://github.com/jack-and-rozz/baba-is-auto that is forked from https://github.com/utilForever/baba-is-auto. 


## Requirements
- python >= 3.7
- cmake >= 3.14.3


## Setup
```
pip install -r requirements.txt

git clone https://github.com/utilForever/baba-is-auto --recursive
cd baba-is-auto 
mkdir build 
cd build 
cmake ..
make 
cd ..
pip install --editable .
```

## How to run
```
# Manual playing
python manual_play.py --map_name [map_name]

# Training a RL agent
python REINFORCE.py [save_dir]

# Save the logs of the trained agent as gif, at each epoch
python create_gif.py [save_dir] --map_name [map_name]
```


## Thanks to
- [Chris Oak](https://github.com/utilForever)