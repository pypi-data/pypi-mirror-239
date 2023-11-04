import argparse
import sys

from iam_cli.command import Command
from iam_cli import VERSION


def get_arguments():
    parser = argparse.ArgumentParser(description="Process a CSV file for IAM users.")
    parser.add_argument('-p', '--profile', dest='profile', action='store', default='default',
                        help='use aws credential profile.')
    parser.add_argument('-v', '--version', action='version', version=f'iam-cli v{VERSION}')
    
    return parser


def main():
    try:
        parser = get_arguments()

        Command()
    except KeyboardInterrupt:
        print('Cancelled by user.')
        sys.exit()


if __name__ == '__main__':
    main()
