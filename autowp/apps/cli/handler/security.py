import click
from typing import NoReturn

from autowp.core.shared.entity import State
from autowp.apps.shared.config import config
from autowp.apps.cli.utils.runner import runner
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.repository.security import SecurityRepository
from autowp.apps.cli.adapter.security.login import LoginAdapter

@click.command('security:login', help='Login using profile name')
@click.argument('name')
@click.option('--password', prompt=True, hide_input=True)
def login(name: str, password: str) -> NoReturn:
	click.echo('=========================')
	click.echo('Logging in profile....')

	def _main():
		repo = ProfileRepository(config())
		repo_sec = SecurityRepository(config())

		# try to run registering process
		security = LoginAdapter(repo, repo_sec, config())
		session = security.login(name, password)

		if isinstance(session, State):
			click.secho('Wrong password or profile name', fg='red')
		else:
			click.secho(f'Login successfull, your token is: {session.token.build().decode()}', fg='green')
		
		click.echo('=========================')

	runner(_main)

@click.command('security:logout', help='Logout')
def logout() -> NoReturn:
	pass

@click.command('security:current', help='Show current logged in profile')
def current() -> NoReturn:
	pass
