import logging

import click

from . import backend_checker
from .logger import set_default_logger


@click.group()
def cli():
    pass


cli.add_command(backend_checker.check_pipeline_status)

if __name__ == '__main__':
    set_default_logger()
    logging.getLogger().setLevel(logging.INFO)
    cli()
