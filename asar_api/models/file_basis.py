import json
from typing import Optional
from pathlib import Path
from pydantic import BaseModel


class GeneralNameSchema(BaseModel):
    name: str
    new_name: Optional[str]


class GeneralObjectSchema(BaseModel):
    pass


class FileBasis():
    def __init__(self,
                 prj_path: Path,
                 file_name: str,
                 default_content: dict = {},
                 name_schema=GeneralNameSchema,
                 object_schema=GeneralObjectSchema) -> None:
        self.prj_path = prj_path
        self.file = prj_path.joinpath(file_name)
        self.name_schema = name_schema
        self.object_schema = object_schema
        self.default_content = default_content

    @property
    def content(self) -> dict:
        return self.read_json()

    @property
    def names(self) -> tuple:
        return tuple(self.content.keys())

    def init(self) -> None:
        self.file.touch()
        self.file.write_text('{}')

    def select(self, name: str):
        # Validate
        _ = self.name_schema(name=name)
        # Implement
        return self.content[name]

    def create(self, name: str, input_content: dict) -> None:
        # Validate
        _ = self.name_schema(name=name)
        valid_content = self.object_schema.parse_obj(
            input_content or self.default_content)
        content = self.content
        if name in content:
            raise ValueError(f'{name} already exists')
        # Implement
        content[name] = json.loads(valid_content.json(exclude_unset=True, exclude_none=True)) # Todo: follow https://github.com/pydantic/pydantic/issues/1409
        self.write_json(content)

    def update(self, name, new_name, input_content) -> None:
        # Validate
        _ = self.name_schema(name=name, new_name=new_name)
        if input_content is not None:
            valid_content = self.object_schema.parse_obj(input_content)
        content = self.content
        if name not in content:
            raise ValueError(f'{name} does not exist')
        elif new_name in content:
            raise ValueError('Duplicate names are not allowed')
        # Implement
        if input_content is not None:
            content[name] = json.loads(valid_content.json(exclude_unset=True)) # Todo: follow https://github.com/pydantic/pydantic/issues/1409
        if new_name:
            content[new_name] = content.pop(name)
        self.write_json(content)

    def delete(self, name) -> None:
        # Validate
        _ = self.name_schema(name=name)
        # Implement
        content = self.content
        del content[name]
        self.write_json(content)

    def read_json(self) -> dict:
        with open(self.file, 'r', encoding="utf-8") as f:
            f_json = json.load(f)
        return f_json

    def write_json(self, f_json: dict) -> dict:
        with open(self.file, 'w', encoding="utf-8") as f:
            json.dump(f_json, f, indent=4, ensure_ascii=False)
