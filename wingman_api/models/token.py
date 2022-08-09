from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from wingman_api.config import (TOKENS_DIR_NAME, 
                                TOKENS_FILE_NAME, 
                                JIEBA_DICT_NAME)
from .file_basis import FileBasis


class Token(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         dir_name=TOKENS_DIR_NAME,
                         file_name=TOKENS_FILE_NAME,
                         object_schema=TokenObjectSchema)
        self.jieba_dict = self.dir.joinpath(JIEBA_DICT_NAME)

    def gen_jieba_dict(self) -> None:
        content = self.content
        with open(file=self.jieba_dict,
                  mode='w',
                  encoding="utf-8") as f:
            for token, v in content.items():
                frequency = v.get('frequency', '')
                f.write(f'{token} {frequency}\n')


class TokenObjectSchema(BaseModel):
    frequency: Optional[int]
