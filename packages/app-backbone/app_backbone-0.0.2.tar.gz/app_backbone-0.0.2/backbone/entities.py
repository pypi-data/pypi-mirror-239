from typing import Any, Generic, Type, TypeVar


T = TypeVar("T")
C = TypeVar("C")


class ComposedObject:
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, base_data, components):
        self.__dict__ = base_data
        self.__components = components

    def __getattr__(self, name: str):
        for component in self.__components:
            if hasattr(component, name):
                return getattr(component, name)

        return super().__getattribute__(name)


class Entity(Generic[T]):
    def __init__(self, base_object: T):
        self.base = base_object
        self.base_type = type(base_object)
        self.components = {}

    def add_component(self, component: C):
        self.components[type(component)] = component

    def get(self, component_type: Type[C]) -> C | None:
        return self.components.get(component_type)

    def get_flattened_object(self, *component_types: Type[C]) -> T | Any:
        composed_type = type(
            self.base_type.__name__, (ComposedObject, self.base_type), {}
        )
        components = tuple(self.get(ct) for ct in component_types)
        return composed_type(vars(self.base), components)
