# GitHub issue count stats

From a given Github repository, obtain day-to-day statistics on open issues, PRs, and bugs.

```
$ issue_counter -h
usage: issue_counter [-h] [-c CONFIG] [-k GITHUB_TOKEN] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the config file. Default: ./config.yml
  -k GITHUB_TOKEN, --github-token GITHUB_TOKEN
                        Github API token. If absent, uses the environment
                        value of GITHUB_TOKEN
  -o OUTPUT, --output OUTPUT
                        Name of the output file. Default: ./results.tsv

```

## Installation

*Note*: This software is not compatible with Python 2.x. Use a Python 3.4+
install.

1. Clone this repo: `git clone https://github.com/shin-/github-issue-counter.git`
2. Run `python setup.py install`.
3. `issue_counter --help`

## Config file format

Here is a sample config file:

```yaml
repo: docker/docker-py
bug_labels:
  - kind/bug
categories:
  - group/api-upgrade
  - group/documentation
  - group/windows
  - level/apiclient
  - level/docker-engine
  - level/dockerclient
start_date: '2016-01-01'
```

- repo: Name of the repository, <org>/<name> format required.
- bug_labels: A list of labels used to mark bugs
- categories: A list of labels marking issue categories. Number of open issues
  for each category will appear in a separate column in the output
- start_date: Only compute issues updated after the `start_date`. By default, all issues
  are taken into account

## Output format

The output file is a TSV format that can easily be imported into any spreadsheet software.

```tsv
date    open_issues     closed_issues   open_prs        closed_prs      open_bugs       closed_bugs     group/api-upgrade       group/documentation     group/windows   level/apiclient level/docker-engine     level/dockerclient
2016-01-02      39      6       15      0       2       2       3       9       00      2       0
2016-01-03      39      6       15      0       2       2       3       9       00      2       0
2016-01-04      39      6       15      0       2       2       3       9       00      2       0
2016-01-05      38      7       14      1       2       2       3       8       00      2       0
2016-01-06      38      7       13      3       2       2       2       8       00      2       0
2016-01-07      38      7       13      3       2       2       2       8       00      2       0
2016-01-08      39      8       13      3       2       2       2       8       00      2       0
2016-01-09      38      9       13      3       2       2       2       8       00      2       0
```