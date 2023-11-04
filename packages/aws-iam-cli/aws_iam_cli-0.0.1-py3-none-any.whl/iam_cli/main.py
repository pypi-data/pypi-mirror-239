import argparse
import sys

from command import process_csv, create_cloudformation_yaml
from __init__ import VERSION


def get_arguments():
    parser = argparse.ArgumentParser(description="Process a CSV file for IAM users.")
    parser.add_argument('-p', '--profile', dest='profile', action='store', default='default',
                        help='use aws credential profile.')
    parser.add_argument('-v', '--version', action='version', version=f'iam-cli v{VERSION}')
    parser.add_argument(
        'csvfile',
        type=argparse.FileType('r', encoding='UTF-8'),
        help='The CSV file containing IAM users information.'
    )
    
    return parser


def main():
    try:
        parser = get_arguments()
        args = parser.parse_args()

        # CSV 파일 처리
        users = process_csv(args.csvfile)
        create_cloudformation_yaml(users)
    except KeyboardInterrupt:
        print('Cancelled by user.')
        sys.exit()


if __name__ == '__main__':
    main()
