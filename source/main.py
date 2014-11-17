import sys
import time
import platform
import traceback

from argparse import ArgumentParser, REMAINDER as rem
from importlib import import_module
from poker_game import PokerGame


def parse_args():
    """
    Parses the arguments from the command line
    :return: An object with command-line arguments as attributes
    """
    parser = ArgumentParser()
    parser.add_argument('--seed', help='A number to provide as a seed to the random number generator')
    parser.add_argument('agents', help='A list of agents to simulate', nargs=rem)
    return parser.parse_args()


def file_name_to_class_name(file_name):
    """
    Converts underscored filenames to Camel-cased class names
    :param file_name: String of the file name, not inclusive of the extension to be parsed
    :return: A camel-cased string equivalent
    """
    components = file_name.title().split('_')
    return ''.join(components)


def main():
    args = parse_args()
    seed = int(args.seed) if args.seed is not None else None
    agents = [getattr(import_module('agents.' + a), file_name_to_class_name(a)) for a in args.agents]

    game = PokerGame(bots=agents, seed=seed)

    start_time = time.time()
    outcome = game.run()
    end_time = time.time()

    print "Result:", outcome
    print "Time elapsed: %0.2f seconds" % (end_time - start_time)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception, e:
        print ""
        traceback.print_exc()

    if platform.system() == 'Windows':
        raw_input('\nPress enter to continue')
