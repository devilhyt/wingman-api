from .model import Model
from .token import Token
from .rule import Rule
from .story import Story
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
import shutil
import re
from pathlib import Path
from pydantic import BaseModel, validator
from ..config import WINGMAN_PRJ_DIR, TRAINING_DATA_FILE_NAME
from .intent import Intent
from .action import Action
from .entity import Entity
from .slot import Slot


class Project:
    prj_root = Path(WINGMAN_PRJ_DIR)

    def __init__(self, project_name) -> None:
        # Validate
        _ = ProjectNameSchema(name=project_name)
        # Implement
        self.prj_name = project_name
        self.prj_root.mkdir(parents=True, exist_ok=True)
        self.prj_path = self.prj_root.joinpath(project_name)
        self.intents = Intent(self.prj_path)
        self.actions = Action(self.prj_path)
        self.entities = Entity(self.prj_path)
        self.slots = Slot(self.prj_path)
        self.stories = Story(self.prj_path)
        self.rules = Rule(self.prj_path)
        self.tokens = Token(self.prj_path)
        self.models = Model(self.prj_path, self.prj_name)
        # Tools
        self.yaml = YAML()

    @staticmethod
    def names() -> tuple:
        return tuple([d.stem for d in Project.prj_root.iterdir() if d.is_dir()])

    def create(self) -> None:
        self.prj_path.mkdir(parents=True, exist_ok=False)
        self.intents.init()
        self.actions.init()
        self.entities.init()
        self.slots.init()
        self.stories.init()
        self.rules.init()
        self.tokens.init()
        self.models.init()

    def rename(self, new_project_name) -> None:
        # Validate
        _ = ProjectNameSchema(name=new_project_name)
        # Implement
        target = self.prj_root.joinpath(new_project_name)
        self.prj_path.rename(target)

    def delete(self) -> None:
        shutil.rmtree(self.prj_path)

    def compile(self) -> None:
        nlu = {'nlu': []}
        domain = {'intents': [], 'entities': []}

        # compile intents
        intents = self.intents.content
        for intent_name, intent in intents.items():
            # nlu
            examples_arr = []
            for example in intent['examples']:
                text = ''
                previous_end = 0
                sorted_labels = sorted(
                    example['labels'], key=lambda d: d['start'])
                for label in sorted_labels:
                    token = label.get('token')
                    entity = label.get('entity')
                    role = label.get('role')
                    group = label.get('group')
                    text += example['text'][previous_end:label['start']]
                    text += f'[{token}]{{"entity": "{entity}"'
                    text += f', "role": "{role}"' if role else ''
                    text += f', "group": "{group}"' if group else ''
                    text += f'}}'
                    previous_end = label['end']
                text += example['text'][previous_end:]
                text += '\n'
                examples_arr.append({'text': LiteralScalarString(text)})
            nlu['nlu'].append(
                {'intent': intent_name, 'examples': examples_arr})

            # domain
            intent.pop('examples')
            if intent:
                domain['intents'].append({intent_name: intent})
            else:
                domain['intents'].append(intent_name)

        # compile entities
        entities = self.entities.content
        for entity_name, entity in entities.items():
            if entity:
                domain['entities'].append({entity_name: entity})
            else:
                domain['entities'].append(entity_name)

        training_data = nlu | domain

        with open(file=self.models.dir.joinpath(TRAINING_DATA_FILE_NAME),
                  mode='w',
                  encoding="utf-8") as y:
            self.yaml.dump(data=training_data, stream=y)

        # compile actions


class ProjectNameSchema(BaseModel):
    name: str

    @validator('name')
    def check_name(cls, name: str):
        if not re.match(r"^\w+$", name):
            raise ValueError('Invalid name')
        return name
