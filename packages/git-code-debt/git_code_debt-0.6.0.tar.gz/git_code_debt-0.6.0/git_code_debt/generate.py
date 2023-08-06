from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import collections
import io
import os.path
import sqlite3
import sys
import yaml

from git_code_debt import options
from git_code_debt.discovery import get_metric_parsers_from_args
from git_code_debt.file_diff_stat import get_file_diff_stats_from_output
from git_code_debt.generate_config import DEFAULT_GENERATE_CONFIG_FILENAME
from git_code_debt.generate_config import GenerateOptions
from git_code_debt.logic import get_metric_mapping
from git_code_debt.logic import get_metric_values
from git_code_debt.logic import get_previous_sha
from git_code_debt.repo_parser import RepoParser
from git_code_debt.write_logic import insert_metric_changes
from git_code_debt.write_logic import insert_metric_values


# pylint:disable=too-many-locals


def get_metrics(diff, metric_parsers):
    def get_all_metrics(file_diff_stats):
        for metric_parser_cls in metric_parsers:
            metric_parser = metric_parser_cls()
            for metric in metric_parser.get_metrics_from_stat(file_diff_stats):
                yield metric

    file_diff_stats = get_file_diff_stats_from_output(diff)
    return list(get_all_metrics(file_diff_stats))


def increment_metric_values(metric_values, metrics):
    for metric in metrics:
        metric_values[metric.name] += metric.value


def load_data(
        database_file,
        repo,
        package_names,
        skip_defaults,
        tempdir_location,
):
    metric_parsers = get_metric_parsers_from_args(package_names, skip_defaults)

    with sqlite3.connect(database_file) as db:
        metric_mapping = get_metric_mapping(db)

        repo_parser = RepoParser(repo, tempdir_location=tempdir_location)

        with repo_parser.repo_checked_out():
            previous_sha = get_previous_sha(db)
            commits = repo_parser.get_commits(since_sha=previous_sha)

            # If there is nothing to check gtfo
            if len(commits) == 1 and previous_sha is not None:
                return

            # Maps metric_name to a running value
            metric_values = collections.defaultdict(int)

            # Grab the state of our metrics at the last place
            compare_commit = None
            if previous_sha is not None:
                compare_commit = commits[0]
                metric_values.update(get_metric_values(
                    db, compare_commit.sha,
                ))
                commits = commits[1:]

            for commit in commits:
                if compare_commit is None:
                    diff = repo_parser.get_original_commit(commit.sha)
                else:
                    diff = repo_parser.get_commit_diff(
                        compare_commit.sha, commit.sha,
                    )

                metrics = get_metrics(diff, metric_parsers)
                increment_metric_values(metric_values, metrics)
                insert_metric_values(db, metric_values, metric_mapping, commit)
                insert_metric_changes(db, metrics, metric_mapping, commit)

                compare_commit = commit


def _add_config_file_options(argument_parser):
    argument_parser.add_argument(
        '--config-filename',
        default=DEFAULT_GENERATE_CONFIG_FILENAME,
    )
    argument_parser.add_argument(
        '--create-config', default=False, action='store_true',
    )


def get_options_from_argparse(argv):
    parser = argparse.ArgumentParser(
        description='Generates metrics from a git repo',
    )
    # optional
    options.add_skip_default_metrics(parser)
    options.add_tempdir_location(parser)
    # positional
    options.add_repo(parser)
    options.add_database(parser)
    options.add_metric_package_names(parser)
    # These are added here so the help message includes them but are unused
    _add_config_file_options(parser)
    args = parser.parse_args(argv)
    return args


def get_options_from_config(argv):
    parser = argparse.ArgumentParser()
    _add_config_file_options(parser)
    args, _ = parser.parse_known_args(argv)

    # Create the config if they'd like us to do that.
    if args.create_config:
        args = get_options_from_argparse(argv)
        # yeah yeah, not really yaml, but this is a good way to validate the
        # config as we write it.
        generate_options = GenerateOptions.from_yaml(vars(args))
        with io.open(args.config_filename, 'w') as config_file:
            yaml.safe_dump(
                generate_options.to_yaml(),
                config_file,
                # We want unicode
                encoding=None,
                default_flow_style=False,
            )

    if not os.path.exists(args.config_filename):
        print('No config file found!  Create one with --create-config.')
        exit(1)

    with io.open(args.config_filename) as config_file:
        return GenerateOptions.from_yaml(yaml.load(config_file))


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if (
            argv == [] and os.path.exists(DEFAULT_GENERATE_CONFIG_FILENAME) or
            '--config-filename' in argv or
            '--create-config' in argv
    ):
        args = get_options_from_config(argv)
    else:
        args = get_options_from_argparse(argv)

    if not os.path.exists(args.database):
        print('Not found: {0}'.format(args.database))
        print('Use git-code-debt-create-tables to create a database.')
        return 1

    load_data(
        args.database,
        args.repo,
        args.metric_package_names,
        args.skip_default_metrics,
        args.tempdir_location,
    )


if __name__ == '__main__':
    exit(main())
