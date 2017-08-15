#!/usr/bin/python

import argparse
import os

from .config import parse_config
from .import_issues import import_issues
from .process_issues import activity_report, process_issues
from .utils import print_error, write_to


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config', default='./config.yml',
        help='Path to the config file. Default: ./config.yml'
    )
    parser.add_argument(
        '-k', '--github-token', default=os.environ.get('GITHUB_TOKEN'),
        help='Github API token. If absent, uses the environment value'
             ' of GITHUB_TOKEN'
    )
    parser.add_argument(
        '-o', '--output', default='./results.tsv',
        help='Name of the output file. Default: ./results.tsv'
    )
    activity = parser.add_argument_group('Activity report')

    activity.add_argument(
        '--activity', action='store_true',
        help='Output an activity report instead of the default aggregate '
             'output.'
    )
    activity.add_argument(
        '-p', '--period', type=int, default=7, metavar='DAYS',
        help='Set the interval period for the activity report in days.'
             ' Default: weekly'
    )

    return parser


def main():
    parser = init_parser()
    args = parser.parse_args()

    config_file = args.config
    github_token = args.github_token
    if not github_token:
        print_error('No Github token provided')

    output_file = args.output

    config_data = parse_config(config_file)
    issues_data = import_issues(
        config_data['repo'].split('/'), github_token,
        config_data.get('start_date')
    )

    if args.activity:
        result = activity_report(issues_data, config_data, args.period)
    else:
        result = process_issues(issues_data, config_data)

    return write_to(output_file, result)

if __name__ == '__main__':
    main()
