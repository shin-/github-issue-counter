#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from .utils import extract_datetime


def process_issues(repo_data, config_data, output_file):
    one_day = datetime.timedelta(days=1)
    now = datetime.datetime.now(datetime.timezone.utc)

    if len(repo_data) == 0:
        raise SystemExit()

    # convert all date strings to datetime objects
    for i in repo_data.keys():
        repo_data[i]['created_at'] = extract_datetime(
            repo_data[i]['created_at']
        )
        if repo_data[i]['closed_at'] is not None:
            repo_data[i]['closed_at'] = extract_datetime(
                repo_data[i]['closed_at']
            )

    # retrieve highest issue number
    last_number = min([int(i) for i in repo_data.keys()])
    first_date = extract_datetime(repo_data[str(last_number)]['created_at'])
    if 'start_date' in config_data:
        first_date = config_data['start_date']

    day = datetime.datetime(
        first_date.year, first_date.month, first_date.day,
        tzinfo=datetime.timezone.utc
    )
    day += one_day

    with open(output_file, 'w') as f:
        f.write(
            'date\topen_issues\tclosed_issues\topen_prs\tclosed_prs\topen_bugs'
            '\tclosed_bugs\t%s\n' % '\t'.join(
                config_data['categories']
            )
        )

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

            output = '%s\t%i\t%i\t%i\t%i\t%i\t%i' % (
                key, open_issue_count, closed_issue_count, open_pr_count,
                closed_pr_count, open_bugs_count, closed_bugs_count
            )

            for cat in config_data['categories']:
                output += '\t%i' % categories[cat]

            f.write(output + '\n')

            day += one_day
