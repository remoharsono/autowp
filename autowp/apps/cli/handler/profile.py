import click
from typing import NoReturn

@click.command('profile:register', help='Register new profile')
@click.argument('name')
@click.argument('password')
def register(name: str, password: str) -> NoReturn:
	pass

@click.command('profile:list', help='List of registered profiles')
def list_profiles() -> NoReturn:
	pass

@click.command('profile:delete', help='Delete profile')
@click.argument('name')
def delete(name: str) -> NoReturn:
	pass
