import argparse, glob
import config

def get_parser():
    parser = argparse.ArgumentParser(
        add_help=True, 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    return parser

def add_common_args(parser):
    return parser

def add_training_args(parser):
    parser.add_argument('model_root', 
                        help='The directory to save the trained model.')
    parser.add_argument('--enable_render', action='store_true', 
                        help='If true, the board during training or testing is displayed.')

    parser.add_argument('--num_episode', type=int, default=10000, help=' ')
    parser.add_argument('--num_steps_per_episode', type=int, default=200, help=' ')
    return parser


def add_evaluation_args(parser):
    map_candidates = [l.split('/')[-1].split('.')[0] for l in glob.glob(config.MAP_ROOT + '/*')]
    parser.add_argument('-map', '--map_name', type=str, default='baba_is_you',
                        choices=map_candidates, help=' ')
    parser.add_argument('--save_gif_path', type=str, default='', help=' ')

    return parser

def get_training_args():
    parser = get_parser()
    parser = add_common_args(parser)
    parser = add_training_args(parser)
    args = parser.parse_args()
    return args

def get_evaluation_args():
    parser = get_parser()
    parser = add_common_args(parser)
    parser = add_evaluation_args(parser)
    args = parser.parse_args()
    args.map_path = config.MAP_ROOT + '/' + args.map_name + '.txt'
    return args


