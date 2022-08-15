import re
from typing import Any, Optional, List
from pathlib import Path
from pydantic import BaseModel, validator, conlist
from wingman_api.config import SLOTS_DIR_NAME, SLOTS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Slot(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content={'type':'any'}
        super().__init__(prj_path=prj_path,
                         dir_name=SLOTS_DIR_NAME,
                         file_name=SLOTS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=SlotNameSchema,
                         object_schema=SlotObjectSchema)

class SlotNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if not re.match(r"^\w+$", name):
                raise ValueError('Invalid name')
        return name

class SlotConditionSchema(BaseModel):
    active_loop : str
    requested_slot: Optional[str]
    
class SlotMappingSchema(BaseModel):
    type: str
    inent: Optional[Any]
    not_inent: Optional[Any]
    entity: Optional[str]
    role: Optional[str]
    group: Optional[str]
    value: Optional[Any]
    action: Optional[str]
    conditions: Optional[List[SlotConditionSchema]]
    

class SlotObjectSchema(BaseModel):
    type: str
    values: Optional[list]
    min_value: Optional[float]
    max_value: Optional[float]
    initial_value: Optional[Any]
    mappings: Optional[List[SlotMappingSchema]]
    
    
