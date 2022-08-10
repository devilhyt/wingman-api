from typing import Dict, Optional, List
from pathlib import Path
from pydantic import BaseModel, root_validator
from wingman_api.config import INTENTS_DIR_NAME, INTENTS_FILE_NAME
from .file_basis import FileBasis


class Intent(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         dir_name=INTENTS_DIR_NAME,
                         file_name=INTENTS_FILE_NAME,
                         object_schema=IntentObjectSchema)


class Label(BaseModel):
    token: str
    start: int
    end: int
    entity: str


class IntentObjectSchema(BaseModel):
    examples: Optional[List[str]]
    labels: Optional[List[Label]]
    use_entities: Optional[List[str]]
    ignore_entities: Optional[List[str]]

    @root_validator
    def check_use_ignore_entities(cls, values: dict):
        if values.get('use_entities') and values.get('ignore_entities'):
            raise ValueError(
                'You can only use_entities or ignore_entities for any single intent.')
        return values
