from backbone.entity_streams import EntityStream, EntityStreamBuilder
from backbone.extensions import Extension, ExtensionLoader


class App:
    def __init__(self):
        self._entity_streams = {}
        self._extensions = {}

    def add_entity_stream(self, entity_stream: EntityStream, name: str | None = None):
        stream_name = type(entity_stream).__name__ if name is None else name
        self._entity_streams[stream_name] = entity_stream

    def add_extension(self, extension: Extension, name: str | None = None):
        extension_name = extension.name if name is None else name
        self._extensions[extension_name] = extension

    @classmethod
    async def create(
        cls,
        extensions: list[ExtensionLoader],
        entity_streams: list[EntityStreamBuilder],
    ) -> "App":
        app = cls()
        for entity_stream_builder in entity_streams:
            app.add_entity_stream(await entity_stream_builder.create_entity_stream())

        for extension_loader in extensions:
            app.add_extension(await extension_loader.load_extension())

        return app
