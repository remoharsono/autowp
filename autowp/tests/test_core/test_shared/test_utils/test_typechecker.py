import unittest

from autowp.core.shared.utils import typechecker
from autowp.core.shared.exceptions import VarTypeError

class TypeCheckerTestCase(unittest.TestCase):

	def test_mismatch(self):
		with self.assertRaises(VarTypeError):
			typechecker.check('test', int, ('test', 'int'))
