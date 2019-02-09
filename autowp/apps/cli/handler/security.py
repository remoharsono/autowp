import click
from typing import NoReturn

@click.command('security:login', help='Login using profile name')
@click.argument('name')
def login(name: str) -> NoReturn:
	pass

@click.command('security:logout', help='Logout')
def logout() -> NoReturn:
	pass

@click.command('security:current', help='Show current logged in profile')
def current() -> NoReturn:
	pass
