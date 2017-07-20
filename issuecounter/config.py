import datetime
import sys

from ruamel.yaml import YAML

from .utils import print_error


def parse_config(config_file):
    with open(config_file, 'r') as f:
        result = YAML(typ='safe').load(f)
    if 'start_date' in result:
        result['start_date'] = datetime.datetime.strptime(
            result['start_date'], '%Y-%m-%d'
        ).replace(tzinfo=datetime.timezone.utc)
    check_config(result)
    return result


def check_config(data):
    if not data.get('repo'):
        print_error('Missing "repo" key in config')
        sys.exit(1)

    if not len(data['repo'].split('/')) == 2:
        print_error('"repo" key must match "org/repo" format')
        sys.exit(1)
