#!/usr/bin/env python

import datetime
import json
import os

import github3

from .utils import DateTimeEncoder
from .utils import extract_datetime


def import_issues(repo, gh_token, max_date=None, cache_folder=','):
    org, repo_name = repo
    issues_file = '{}/{}_issues.json'.format(cache_folder, org)
    data = {}

    if os.path.isfile(issues_file):
        with open(issues_file) as f:
            data = json.load(f)

    gh = github3.login(token=gh_token)

    if repo_name not in data.keys():
        data[repo_name] = {}

    since = last_import_date(data[repo_name])
    if max_date:
        since = max(max_date, since)
    for i in gh.iter_repo_issues(org, repo_name, state='all', since=since):
        print('Processing issue #%s' % i.number)
        data[repo_name][str(i.number)] = {
            'created_at': i.created_at,
            'closed_at': i.closed_at,
            'is_pull_request': (i.pull_request is not None),
            'labels': [l.name for l in i.labels]
        }
    with open(issues_file, 'w') as f:
        json.dump(data, f, cls=DateTimeEncoder)

    return data[repo_name]


def last_import_date(repo_data):
    seq = repo_data.keys()
    if len(seq) > 0:
        max_issue_number = str(max([int(k) for k in seq]))
        return extract_datetime(repo_data[max_issue_number]['created_at'])

    return datetime.datetime.fromtimestamp(0, datetime.timezone.utc)
