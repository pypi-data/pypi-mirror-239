from pathlib import Path
from typing import Generator, Protocol
from importlib.util import spec_from_file_location, module_from_spec
import sys


class Extension:
    def __init__(self, module_name: str, module_path: Path):
        self.name = module_name
        self.path = module_path


class ExtensionLoader(Protocol):
    async def load_extension(self) -> Extension:
        ...


class ModulePathExtensionLoader:
    def __init__(self, module_path: Path):
        self.path = module_path

    async def load_extension(self) -> Extension:
        module_name = self.path.stem
        if module_name == "__init__":
            module_name = self.path.parent.stem

        spec = spec_from_file_location(module_name, self.path.resolve())
        module = module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return Extension(module_name, self.path)

    @classmethod
    def find_extensions_in_directory(
        cls, directory_path: Path
    ) -> "Generator[ModulePathExtensionLoader, None, None]":
        for module_path in directory_path.iterdir():
            if module_path.stem[0] in {".", "_"}:
                continue

            if module_path.is_file():
                yield cls(module_path)

            elif (module_path / "__init__.py").exists():
                yield cls(module_path / "__init__.py")
