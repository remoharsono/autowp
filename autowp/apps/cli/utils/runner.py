import click
from typing import Callable, NoReturn, Optional

from autowp.apps.shared.base.exceptions import ConfigError
from autowp.core.shared.exceptions import ValidationError, VarTypeError, StorageError

Callback = Callable[[None], None]

def runner(main_cb: Callback, success_cb: Optional[Callback] = None) -> NoReturn:
	"""Used to run main handler process"""
	try:
		main_cb()
	except ValidationError as exc_validation:
		# do something when validation failed
		click.secho(f'Your input is not valid: {exc_validation}', fg='red')
		click.echo('=========================')
	except VarTypeError as exc_vartype:
		# do something when there are mismatch variable types
		click.secho(f'Mismatch variable type: {exc_vartype}', fg='red')
		click.echo('=========================')
	except StorageError as exc_storage:
		# do something when there is an error related with database
		click.secho(f'Error data storage: {exc_storage}', fg='red')
		click.echo('=========================')
	except ConfigError as exc_config:
		msg = exc_config.get_message() 
		click.secho(f'Error config: {msg}', fg='red')
		click.echo('=========================')
	except NameError as exc_name_err:
		click.secho(f'Naming error: {exc_name_err}', fg='red')
		click.echo('=========================')
	except TypeError as exc_type_err:
		click.secho(f'Type error: {exc_type_err}', fg='red')
		click.echo('=========================')
	else:
		if success_cb:
			success_cb()
