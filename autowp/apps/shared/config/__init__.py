from autowp.apps.shared.config.data import Config
from autowp.apps.shared.config.parser import Parser

def config() -> Config:
	"""Parse and load config"""
	parser = Parser(Config)
	return parser.config
