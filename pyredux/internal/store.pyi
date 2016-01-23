from typing import Any, Callable, Dict

class BaseStore:
    def dispatch(self, action: Dict) -> Dict: pass
    def get_state(self) -> Any: pass

class Store(BaseStore):
    def subscribe(self, listener: Callable[Callable[Dict], Callable]) -> Callable: pass
    def replace_reducer(self, reducer: Callable[Any, Dict]) -> None: pass