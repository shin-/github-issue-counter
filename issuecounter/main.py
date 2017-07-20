#!/usr/bin/python

import argparse
import os

from .config import parse_config
from .import_issues import import_issues
from .process_issues import process_issues
from .utils import print_error


def main():
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
    process_issues(issues_data, config_data, output_file)

if __name__ == '__main__':
    main()
