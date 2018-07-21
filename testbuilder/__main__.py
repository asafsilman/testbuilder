"""
Invoke testbuilder commandline utility.

Example: python -m testbuilder <command>
"""

import click

from testbuilder.core import management

@click.group()
def cli():
    pass

@click.command()
@click.argument('file', required=True, metavar="<file>")
@click.option('--file-type', '-t', default="excel", type=click.Choice(["excel", "yaml"]))
@click.option('--profile', '-p', default="default")
def run(file, file_type, profile):
    management.run_test_case(file, file_type, profile)

@click.command()
@click.option('--verbose', '-v', is_flag=True)
def test(verbose):
    management.run_unittests(verbose)

cli.add_command(run)
cli.add_command(test)

if __name__=="__main__":
    cli(prog_name="python -m testbuilder") #pylint: disable=E1123
