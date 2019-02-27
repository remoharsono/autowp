import unittest
import uuid
from typing import Any, Dict, Optional, List, NoReturn
from dataclasses import asdict

from autowp.core.shared.exceptions import ValidationError
from autowp.core.resource.entity import Server
from autowp.core.resource.repository import ResourceRepository 
from autowp.core.resource.utils.validation import ValidateResource

class FakeRepo(ResourceRepository):
	def __init__(self, memory: Dict[str, Any]):
		self.memory = memory

	def create(self, server: Server) -> Optional[Server]:
		mem_id = uuid.uuid4()
		self.memory[str(mem_id)] = server
	
	def update(self, conditions: Dict[str, Any], doc: Dict[str, Any]) -> Optional[Server]:
		pass
	
	def get_list(self, options: Optional[Dict[str, Any]] = None) -> Optional[List[Server]]:
		pass

	def findById(self, id: str) -> Optional[Server]:
		pass

	def findByField(self, field: str, value: Any) -> Optional[Server]:
		if not self.memory:
			return None

		for k, v in self.memory.items():
			data = asdict(v)
			for key, val in data.items():
				if key == field:
					if val == value:
						return v 

		return None
	
	def remove(self, id: str) -> NoReturn:
		pass

class ValidationTestCase(unittest.TestCase):

	def test_validation_passed(self):
		memory = {}
		repo = FakeRepo(memory)
		validation = ValidateResource()

		server = Server(profile_id='profile_id', host='host', user='user')

		# should not throw any exceptions
		validation.validate(server, repo=repo)

	def test_validation_fail_no_profile_id(self):
		memory = {}
		repo = FakeRepo(memory)
		validation = ValidateResource()

		server = Server(host='host', user='user', profile_id='')
		with self.assertRaises(ValidationError):
			# should not throw any exceptions
			validation.validate(server, repo=repo)
		
		server = Server(host='host', user='user', profile_id=None)
		with self.assertRaises(ValidationError):
			# should not throw any exceptions
			validation.validate(server, repo=repo)

	def test_validation_fail_no_host(self):
		memory = {}
		repo = FakeRepo(memory)
		validation = ValidateResource()

		server = Server(profile_id='profile_id', user='user', host='')
		with self.assertRaises(ValidationError):
			# should not throw any exceptions
			validation.validate(server, repo=repo)
		
		server = Server(profile_id='profile_id', user='user', host=None)
		with self.assertRaises(ValidationError):
			# should not throw any exceptions
			validation.validate(server, repo=repo)

	def test_validation_fail_host_registered(self):
		memory = {}
		repo = FakeRepo(memory)
		validation = ValidateResource()

		server = Server(profile_id='profile_id', host='host', user='user')

		# should not throw any exceptions
		validation.validate(server, repo=repo)
		repo.create(server)

		with self.assertRaises(ValidationError):
			# should not throw any exceptions
			validation.validate(server, repo=repo)

	def test_validation_fail_no_user(self):
		memory = {}
		repo = FakeRepo(memory)
		validation = ValidateResource()

		server = Server(profile_id='profile_id', host='host', user='')
		with self.assertRaises(ValidationError):
			# should not throw any exceptions
			validation.validate(server, repo=repo)

		server = Server(profile_id='profile_id', host='host', user=None)
		with self.assertRaises(ValidationError):
			# should not throw any exceptions
			validation.validate(server, repo=repo)
