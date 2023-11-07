from typing import Any, Callable, Dict, List, Optional, Tuple

from seaplane.errors import SeaplaneError
from seaplane.logs import log

from .tasks import OpenAI, Replicate, Store, SubstationTask


class TaskEvent:
    def __init__(self, id: str, input: Any) -> None:
        self.id = id
        self.status = "in_progress"
        self.input = input
        self.output: Optional[Any] = None
        self.error: Optional[Any] = None

    def set_output(self, output: Any) -> None:
        self.output = output
        self.status = "completed"

    def set_error(self, error: Any) -> None:
        self.error = error
        self.status = "error"


SEAPLANE_API_KEY_NAME = "SEAPLANE_API_KEY"
OPENAI_API_KEY_NAME = "OPENAI_API_KEY"
REPLICATE_API_KEY_NAME = "REPLICATE_API_KEY"


class Task:
    def __init__(
        self,
        func: Callable[[Any], Any],
        type: str,
        id: Optional[str] = None,
        model: Optional[str] = None,
        index_name: Optional[str] = None,
        replicas: Optional[int] = 1,
    ) -> None:
        self.func = func
        self.args: Optional[Tuple[Any, ...]] = None
        self.kwargs: Optional[Dict[str, Any]] = None
        self.type = type
        self.model = model
        self.sources: List[str] = []
        self.name = func.__name__
        self.index_name = index_name
        self.replicas = replicas

        if id is not None:
            self.id = id
        else:
            self.id = func.__name__

    def process(self, *args: Any, **kwargs: Any) -> Any:
        self.args = args
        self.kwargs = kwargs

        log.info(f"Task type '{self.type}' Model ID {self.model}")

        if self.type == "vectordb":
            log.info("Accessing Vector DB task...")

            if not self.index_name:
                raise SeaplaneError("Missing index_name attribute on vectordb Task.")

            self.args = self.args + (Store(self.index_name),)
            return self.func(*self.args, **self.kwargs)

        model = None

        if self.model:
            model = self.model.lower()
        else:
            model = self.model

        if model == "mpt-30b":
            substation = SubstationTask(self.func, self.id, model)
            return substation.process(*self.args, **self.kwargs)
        elif model == "gpt-3.5":
            openai = OpenAI(self.func, self.id, model)
            return openai.process(*self.args, **self.kwargs)
        elif model == "gpt-3":
            openai = OpenAI(self.func, self.id, model)
            return openai.process(*self.args, **self.kwargs)
        elif model == "stable-diffusion":
            replicate = Replicate(self.func, self.type, self.id, model)
            return replicate.process(*self.args, **self.kwargs)
        elif model:
            replicate = Replicate(self.func, self.type, self.id, model)
            return replicate.process(*self.args, **self.kwargs)
        else:
            log.info("Compute task type...")
            return self.func(*self.args, **self.kwargs)

    def called_from(self, sources: List[str]) -> None:
        self.sources = sources

    def print(self) -> None:
        log.info(f"id: {self.id}, type: {self.type}, model: {self.model}")
