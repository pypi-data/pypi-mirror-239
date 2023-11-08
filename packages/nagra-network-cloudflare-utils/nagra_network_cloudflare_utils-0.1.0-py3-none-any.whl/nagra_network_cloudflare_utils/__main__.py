import logging

import click
from nagra_network_misc_utils.logger import set_default_logger

from .compliance import remove_cloudflare_records
from .dns_checker import check_csvfile
from .list_zones import list_zones

set_default_logger()
logging.getLogger().setLevel(logging.INFO)


@click.group()
def cli():
    pass


cli.add_command(check_csvfile)
cli.add_command(remove_cloudflare_records)
cli.add_command(list_zones)

if __name__ == '__main__':
    cli()
