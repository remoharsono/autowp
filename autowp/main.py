import argparse

parser = argparse.ArgumentParser(prog='autowp', description='CLI app to helping people manage their wp sites')
subparsers = parser.add_subparsers(title='Commands', metavar='')

# profile app
profile_register = subparsers.add_parser('profile:register', description='Register new profile', help='')
profile_register.add_argument('--name', default=None, help='Choose profile name', dest='profile_register:name')
profile_register.add_argument('--password', default=None, help='Choose password', dest='profile_register:password')

profile_list = subparsers.add_parser('profile:list', description='List of registered profiles', help='')
profile_list.add_argument('--run', action='store_true', default=False, dest='profile_list:run')

profile_delete = subparsers.add_parser('profile:delete', description='Delete selected profile', help='')
profile_delete.add_argument('--name', default=None, help='Choose profile name to delete', dest='profile_delete:name')

# security app
security_login = subparsers.add_parser('security:login', description='Login using profile', help='')
security_login.add_argument('--name', default=None, help='Choose profile name to login', dest='security_login:name')

security_logout = subparsers.add_parser('security:logout', description='Delete current session', help='')
security_logout.add_argument('--run', action='store_true', default=False, dest='security_logout:run')

security_current = subparsers.add_parser('security:current', description='Get current profile identity', help='')
security_current.add_argument('--run', action='store_true', default=False, dest='security_current:run')

if __name__ == '__main__':
	args = parser.parse_args()
	command = args._get_kwargs()
	print(command)
