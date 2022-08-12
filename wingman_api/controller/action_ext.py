import json
from pathlib import Path
from flask import Flask, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.config import WINGMAN_ROOT

actions_root = Path(WINGMAN_ROOT, 'wingman_api', 'assets', 'actions')


class ActionTypeAPI(MethodView):
    """Wingman Action Type API"""
    decorators = [jwt_required()]

    def get(self):
        """Get the names of all action types"""
        # Implement
        type_names = [d.stem for d in actions_root.iterdir() if d.is_dir()]
        return jsonify(type_names)


class ActionSchemaAPI(MethodView):
    """Wingman Action Schema API"""
    decorators = [jwt_required()]

    def get(self, type_name):
        """Get the schema of an action type"""
        type_names = [d.stem for d in actions_root.iterdir() if d.is_dir()]
        if type_name not in type_names:
            raise ValueError('Action type does not exist')

        schema_file = actions_root.joinpath(type_name, 'schema.json')

        # Implement
        with open(schema_file, 'r', encoding="utf-8") as json_file:
            schema_json = json.load(json_file)

        return jsonify(schema_json), 200


def init_app(app: Flask):
    action_type_view = ActionTypeAPI.as_view('action_type_api')
    app.add_url_rule('/actions/types',
                     view_func=action_type_view,
                     methods=['GET'])
    action_schema_view = ActionSchemaAPI.as_view('action_schema_api')
    app.add_url_rule('/actions/schema/<string:type_name>',
                     view_func=action_schema_view,
                     methods=['GET'])
