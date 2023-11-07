from backbone.entities import Entity


try:
    from asyncio import TaskGroup
except ImportError:
    from backbone.vendored.task_groups import TaskGroup

from weakref import WeakSet
from typing import Callable, Coroutine, Protocol, TypeAlias


Consumer: TypeAlias = Callable[[Entity], Coroutine[None, None, None]]


class EntityStream:
    def __init__(self):
        self._consumers: WeakSet[Consumer] = WeakSet()

    async def push(self, entity: Entity):
        async with TaskGroup() as group:
            for consumer in self._consumers:
                group.create_task(consumer(entity))

    def add_consumer(self, callback: Consumer):
        self._consumers.add(callback)


class EntityStreamBuilder(Protocol):
    async def create_entity_stream(self) -> EntityStream:
        ...
