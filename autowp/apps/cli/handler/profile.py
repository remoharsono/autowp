import click
from terminaltables import AsciiTable 
from typing import NoReturn

from autowp.apps.shared.config import config
from autowp.apps.cli.utils.runner import runner
from autowp.apps.cli.repository.profile import ProfileRepository

from autowp.apps.cli.adapter.profile.register import RegisterAdapter 
from autowp.apps.cli.adapter.profile.delete import DeleteAdapter 
from autowp.apps.cli.adapter.profile.profiles import ProfilesAdapter 

@click.command('profile:register', help='Register new profile')
@click.argument('name')
@click.argument('password')
def register(name: str, password: str) -> NoReturn:
	
	click.echo('=========================')
	click.echo('Registering new profile....')

	def _main():
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)

		# try to run registering process
		profile = adapter.register(name, password)

	def _success():
		# registering profile should be success here
		click.echo(f'Your profile: {name}, has been registered')
		click.echo('=========================')

	# run process
	runner(_main, _success)

@click.command('profile:list', help='List of registered profiles')
def list_profiles() -> NoReturn:
	click.echo('=========================')
	click.echo(f'List profiles...')
	
	repo = ProfileRepository(config())
	adapter = ProfilesAdapter(repo)
	profiles = adapter.all()

	if not profiles:
		click.secho('You doesnt have any profiles', fg='green')
	else:
		table_data = []
		table_data.append(['Profile names'])

		for profile in profiles:
			table_data.append([profile.name])

		table = AsciiTable(table_data)
		print(table.table)
	
	click.echo('=========================')

@click.command('profile:delete', help='Delete profile')
@click.argument('name')
def delete(name: str) -> NoReturn:
	click.echo('=========================')
	click.echo(f'Deleting profile...')

	repo = ProfileRepository(config())
	adapter = DeleteAdapter(repo)
	adapter.remove(name)

	click.echo(f'Your profile: {name}, has been deleted')
	click.echo('=========================')
