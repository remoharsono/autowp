from autowp.apps.cli.processor import cli
from autowp.apps.cli.handler import profile, security

if __name__ == '__main__':
	# profile management
	cli.add_command(profile.register)
	cli.add_command(profile.list_profiles)
	cli.add_command(profile.delete)

	# security management
	cli.add_command(security.login)
	cli.add_command(security.logout)
	cli.add_command(security.current)

	# run main cli apps
	cli()
