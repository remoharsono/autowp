import unittest
import jwt

from autowp.apps.shared.security.tokenizer import JWTToken

class JWTTokenTestCase(unittest.TestCase):

	def test_encode_success(self):
		payload = {'name': 'testing'}
		salt = 'test_salt'

		tokenizer = JWTToken(salt, payload) 
		token = tokenizer.encode()

		decoded = tokenizer.decode(token)
		self.assertEqual(payload.get('name'), decoded.get('name'))
