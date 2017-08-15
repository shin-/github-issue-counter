#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from .utils import extract_datetime


def _convert_dates(repo_data):
    for i in repo_data.keys():
        repo_data[i]['created_at'] = extract_datetime(
            repo_data[i]['created_at']
        )
        if repo_data[i]['closed_at'] is not None:
            repo_data[i]['closed_at'] = extract_datetime(
                repo_data[i]['closed_at']
            )

    return repo_data


def activity_report(repo_data, config_data, interval=7):
    one_day = datetime.timedelta(days=1)
    period = datetime.timedelta(days=interval)
    now = datetime.datetime.now(datetime.timezone.utc)
    output_data = []

    if len(repo_data) == 0:
        raise SystemExit()

    repo_data = _convert_dates(repo_data)

    # retrieve highest issue number
    last_number = min([int(i) for i in repo_data.keys()])
    first_date = config_data.get('start_date') or extract_datetime(
        repo_data[str(last_number)]['created_at']
    )

    day = datetime.datetime(
        first_date.year, first_date.month, first_date.day,
        tzinfo=datetime.timezone.utc
    )
    day += one_day
    header = [
        'date',
        'open_issues',
        'closed_issues',
        'open_prs',
        'closed_prs',
        'open_bugs',
        'closed_bugs'
    ]
    for cat in config_data['categories']:
        header.append('open:{}'.format(cat))
        header.append('closed:{}'.format(cat))
    output_data.append(header)

    while day < now:
        key = day.strftime('%Y-%m-%d')
        print(key)

        open_pr_count = 0
        closed_pr_count = 0
        open_issue_count = 0
        closed_issue_count = 0
        open_bugs_count = 0
        closed_bugs_count = 0
        categories = {}
        for cat in config_data['categories']:
            categories[cat] = [0, 0]

        for i in repo_data:
            element = repo_data[i]

            if element['created_at'] > day + period:
                continue

            if element['closed_at'] and element['closed_at'] < day:
                continue

            closed = False
            opened = False

            if element['created_at'] >= day:
                opened = True

            if element['closed_at'] and element['closed_at'] < day + period:
                closed = True

            if element['is_pull_request']:
                if opened:
                    open_pr_count += 1
                if closed:
                    closed_pr_count += 1
            else:
                if opened:
                    open_issue_count += 1
                if closed:
                    closed_issue_count += 1

            for label in config_data['bug_labels']:
                if label in element['labels']:
                    if opened:
                        open_bugs_count += 1
                    if closed:
                        closed_bugs_count += 1
                    break

                for cat in config_data['categories']:
                    if cat in element['labels']:
                        if opened:
                            categories[cat][0] += 1
                        if closed:
                            categories[cat][1] += 1

        line = [
            key, open_issue_count, closed_issue_count, open_pr_count,
            closed_pr_count, open_bugs_count, closed_bugs_count
        ]

        for cat in config_data['categories']:
            line.append(categories[cat][0])
            line.append(categories[cat][1])

        output_data.append(line)

        day += period

    return output_data


def process_issues(repo_data, config_data):
    one_day = datetime.timedelta(days=1)
    now = datetime.datetime.now(datetime.timezone.utc)
    output_data = []
    if len(repo_data) == 0:
        raise SystemExit()

    # convert all date strings to datetime objects
    repo_data = _convert_dates(repo_data)

    # retrieve highest issue number
    last_number = min([int(i) for i in repo_data.keys()])
    first_date = config_data.get('start_date') or extract_datetime(
        repo_data[str(last_number)]['created_at']
    )

    day = datetime.datetime(
        first_date.year, first_date.month, first_date.day,
        tzinfo=datetime.timezone.utc
    )
    day += one_day

    # Table header
    output_data.append([
        'date',
        'open_issues',
        'closed_issues',
        'open_prs',
        'closed_prs',
        'open_bugs',
        'closed_bugs'
    ] + config_data['categories'])

    while day < now:
        key = day.strftime('%Y-%m-%d')
        print(key)

        open_pr_count = 0
        closed_pr_count = 0
        open_issue_count = 0
        closed_issue_count = 0
        open_bugs_count = 0
        closed_bugs_count = 0
        categories = {}
        for cat in config_data['categories']:
            categories[cat] = 0

        for i in repo_data:
            element = repo_data[i]

            if element['created_at'] > day:
                continue

            is_open = True
            if isinstance(element['closed_at'], datetime.datetime) and (
                    element['closed_at'] < day):
                is_open = False
            if element['is_pull_request']:
                if is_open:
                    open_pr_count += 1
                else:
                    closed_pr_count += 1
            else:
                if is_open:
                    open_issue_count += 1
                else:
                    closed_issue_count += 1

            for label in config_data['bug_labels']:
                if label in element['labels']:
                    if is_open:
                        open_bugs_count += 1
                    else:
                        closed_bugs_count += 1
                    break

                for cat in config_data['categories']:
                    if cat in element['labels']:
                        categories[cat] += 1 if is_open else 0

        line = [
            key, open_issue_count, closed_issue_count, open_pr_count,
            closed_pr_count, open_bugs_count, closed_bugs_count
        ]

        for cat in config_data['categories']:
            line.append(categories[cat])

        output_data.append(line)

        day += one_day

    return output_data
