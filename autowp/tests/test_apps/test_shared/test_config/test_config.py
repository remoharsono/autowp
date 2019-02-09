import unittest

from autowp.apps.shared.config import config
from autowp.apps.shared.config.data import Config

class TestConfigTestCase(unittest.TestCase):

	def test_load_config(self):
		conf = config()
		self.assertIsInstance(conf, Config)
