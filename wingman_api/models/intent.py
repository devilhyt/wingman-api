from pathlib import Path
from wingman_api.config import INTENTS_FILE_NAME
from .file_basis import FileBasis
from pydantic import BaseModel, root_validator
from typing import (Optional, List)


class Intent(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('intents', INTENTS_FILE_NAME),
                         object_schema=IntentObjectSchema)


class IntentObjectSchema(BaseModel):
    examples: Optional[List[str]]
    use_entities: Optional[List[str]]
    ignore_entities: Optional[List[str]]

    @root_validator
    def check_use_ignore_entities(cls, values):
        if values.get('use_entities') and values.get('ignore_entities'):
            raise ValueError(
                'You can only use_entities or ignore_entities for any single intent.')
        return values
