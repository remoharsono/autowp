import click
from typing import NoReturn

from autowp.apps.shared.config import config
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.adapter.profile.register import RegisterAdapter

@click.command('profile:register', help='Register new profile')
@click.argument('name')
@click.argument('password')
def register(name: str, password: str) -> NoReturn:
	adapter = RegisterAdapter(ProfileRepository(config()))

@click.command('profile:list', help='List of registered profiles')
def list_profiles() -> NoReturn:
	pass

@click.command('profile:delete', help='Delete profile')
@click.argument('name')
def delete(name: str) -> NoReturn:
	pass
