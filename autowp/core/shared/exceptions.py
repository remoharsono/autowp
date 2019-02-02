from typing import NoReturn, List, NewType, Dict

# Define new type definitions
ValidationErrorMessage = NewType('ValidationErrorMessage', str)
ValidationErrorMessages = Dict[str, List[ValidationErrorMessage]] 

class Error(Exception):
	"""Base error for this module
	
	Attributes:
		message: An error message
	"""
	def get_message(self) -> str:
		"""Get error message"""
		return self.message

class VarTypeError(Error):
	"""Used when given variable not an instance of some object

	Attributes:
		varname: A variable name in string
		objname: An object name in string
		message: Error message in string
	"""
	def __init__(self, varname: str, objname: str) -> NoReturn:
		self.varname = varname
		self.objname = objname
		self.message = f'A given {varname} is not an instance of {objname}' 

class StorageError(Error):
	"""Used when there is an exception related with data storage

	Attributes:
		message: An error message
	"""
	def __init__(self, message: str) -> NoReturn:
		self.message = message

class ValidationError(Error):
	"""Used when need a raise an error related with validation process
	
	Example error message:
		{
			'field1': ['error message 1', 'error message 2'],
			'field2': ['error message 1]
		}

	Attributes:
		errors: A ValidationErrors
	"""
	def __init__(self, errors: ValidationErrorMessages) -> NoReturn:
		self.errors = errors
		self.message = f'There is at least {len(errors)} error messages, please check errors for more detail'
