from typing import Any, NoReturn, Tuple
from autowp.core.shared.exceptions import VarTypeError

def check(name: Any, obj: Any, desc: Tuple[str, str]) -> NoReturn:
	if not isinstance(name, obj):
		raise VarTypeError(desc[0], desc[1])
