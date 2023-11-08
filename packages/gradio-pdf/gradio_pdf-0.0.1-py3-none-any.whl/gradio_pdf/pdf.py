from __future__ import annotations

from gradio.components.base import Component
from gradio.data_classes import FileData
from gradio import processing_utils

class PDF(Component):

    data_model = FileData

    def preprocess(self, payload: FileData) -> str:
        return payload.path

    def postprocess(self, value: str | None) -> FileData:
        if not value:
            return None
        return FileData(path=value)

    def example_inputs(self):
        return {"foo": "bar"}

    def api_info(self):
        return {"type": {}, "description": "any valid json"}

    def as_example(self, input_data: str | None) -> str | None:
        if input_data is None:
            return None
        return processing_utils.move_resource_to_block_cache(input_data, self)