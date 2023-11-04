import click
from pathlib import Path
import tomllib
import os
import time
import re
import numpy as np
import subprocess
from datetime import datetime

#  ──────────────────────────────────────────────────────────────────────────
# global variables

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)

#  ──────────────────────────────────────────────────────────────────────────
# global functions

def logbook_not_found(name):
    click.echo(name + ' logbook not found in config.')
    exit()

#  ──────────────────────────────────────────────────────────────────────────
# base command

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--config', default='~/.config/dlog.toml', type=str, help="Config file path", show_default=True)
@click.pass_context
def dlog(ctx, config):
    """Simple and quick logging program."""

    ctx.ensure_object(dict)

    config = Path(config).expanduser()
    if config.exists():

        with open(config, 'rb') as file:
            toml = tomllib.load(file)

        # required config options
        required = ['logbooks']
        for option in required:
            if option not in toml:
                click.echo('Config requires "' + key + '" to be set.')
                exit()

        # home log directory
        if 'home' in toml:
            ctx.obj['home'] = Path(toml['home']).expanduser()
        else:
            ctx.obj['home'] = Path('~/dlogs').expanduser()

        # individual logs
        ctx.obj['logbooks'] = []
        for logbook in toml['logbooks']:
            ctx.obj['logbooks'].append(logbook)

            logbook_path = ctx.obj['home'] / Path(logbook)

            if not logbook_path.exists():
                os.mkdir(logbook_path)

        # editor
        if 'editor' in toml:
            ctx.obj['editor'] = toml['editor']
        else:
            ctx.obj['editor'] = 'vim'

    else:
        click.echo('No config file, exiting.')
        exit()

#  ──────────────────────────────────────────────────────────────────────────
# log command to generate single logs

@dlog.command('log', short_help='Open a new log in your editor.',context_settings=CONTEXT_SETTINGS)
@click.argument('name', type=str)
@click.pass_context
def log(ctx, name):
    """Open a new log in the NAME's logbook in your editor."""

    if name in ctx.obj['logbooks']:
        logbook_path = ctx.obj['home'] / Path(name)

        epoch = str(np.floor(time.time()).astype(np.int64))
        date = time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime())

        file_path = logbook_path / Path(epoch + '.md')
        with open(file_path, 'a') as file:
            file.write('# ' + date + '\n')

        click.edit(filename=file_path, editor=ctx.obj['editor'])

    else:
        logbook_not_found(name)

#  ──────────────────────────────────────────────────────────────────────────
# list command to list logs

@dlog.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def list(ctx):
    """Lists all logbooks."""

    for logbook in ctx.obj['logbooks']:
        click.echo(logbook)

    exit()

#  ──────────────────────────────────────────────────────────────────────────
# search command

@dlog.command('search', short_help='Searches through your logs.', context_settings=CONTEXT_SETTINGS)
@click.option('-n', '--name', type=str, help="Specified logbook to search.", default=None)
@click.argument('regex', type=str)
@click.pass_context
def search(ctx, regex, name):
    """
    Searches through your logs for the given REGEX. Searches through all logs unless one is specified. Results are printed as:

    logbook: filename: date: line number: line
    """

    def inbook(ctx, name, regex):

        logbook_path = ctx.obj['home'] / Path(name)
        file_paths = sorted(logbook_path.glob('*.md'))

        for file_path in file_paths:

            date = datetime.utcfromtimestamp(int(file_path.stem)).isoformat()

            with open(file_path, 'r') as file:

                for i, line in enumerate(file):

                    if re.search(regex, line):
                        found_line = name + ': ' + file_path.stem + ': ' + date + ': ' + str(i + 1) + ': ' + line.strip('\n')
                        click.echo(found_line)


    if name:
        if name in ctx.obj['logbooks']:
            inbook(ctx, name, regex)
        else:
            logbook_not_found(name)

    else:
        for name in ctx.obj['logbooks']:
            inbook(ctx, name, regex)

#  ──────────────────────────────────────────────────────────────────────────
# git command

@dlog.command('git', short_help='Git manage the logbooks.', context_settings=CONTEXT_SETTINGS)
@click.argument('git_commands', type=str, nargs=-1)
@click.pass_context
def git(ctx, git_commands):
    """Git command to manage the douglog git repository."""

    command = ['git', '-C', ctx.obj['home']]

    for arg in git_commands:
        command.append(arg)

    subprocess.run(command)
