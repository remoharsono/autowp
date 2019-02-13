import click
from typing import Callable, NoReturn

from autowp.apps.shared.base.exceptions import ConfigError
from autowp.core.shared.exceptions import ValidationError, VarTypeError, StorageError

Callback = Callable[[None], None]

def runner(main_cb: Callback, success_cb: Callback) -> NoReturn:
	"""Used to run main handler process"""
	try:
		main_cb()
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
		success_cb()
