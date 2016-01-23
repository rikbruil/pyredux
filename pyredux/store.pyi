from typing import Any, Callable, Dict
from pyredux.internal.store import Store

def create(
        reducer: Callable[Any, Dict],
        initial_state: Any
) -> Store: pass
