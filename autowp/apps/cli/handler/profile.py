import click
from typing import NoReturn

from autowp.core.shared.exceptions import ValidationError, VarTypeError, StorageError
from autowp.apps.shared.config import config
from autowp.apps.shared.base.exceptions import ConfigError
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.adapter.profile.register import RegisterAdapter 

@click.command('profile:register', help='Register new profile')
@click.argument('name')
@click.argument('password')
def register(name: str, password: str) -> NoReturn:
	
	click.echo('=========================')
	click.echo('Registering new profile....')

	try:
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)

		# try to run registering process
		profile = adapter.register(name, password)
	except ValidationError as exc_validation:
		# do something when validation failed
		click.secho('Your input is not valid', fg='red')
		click.echo('=========================')
	except VarTypeError as exc_vartype:
		# do something when there are mismatch variable types
		click.secho('Mismatch variable type', fg='red')
		click.echo('=========================')
	except StorageError as exc_storage:
		# do something when there is an error related with database
		click.secho('Error data storage', fg='red')
		click.echo('=========================')
	except ConfigError as exc_config:
		click.secho(exc_config.get_message(), fg='red')
		click.echo('=========================')
	else:
		# registering profile should be success here
		click.echo(f'Your profile: {name}, has been registered')
		click.echo('=========================')

@click.command('profile:list', help='List of registered profiles')
def list_profiles() -> NoReturn:
	pass

@click.command('profile:delete', help='Delete profile')
@click.argument('name')
def delete(name: str) -> NoReturn:
	pass
