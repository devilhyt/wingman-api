from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class StoryAPI(MethodView):
    """Wingman Story API"""

    @jwt_required()
    def get(self, project_name, story_name):
        """
        :param story_name:
            If story_name is None, then retrieve all story names.\n
            If story_name is not None, then get a story.
        """

        prj = Project(project_name)
        if story_name:
            story_obj = prj.story.content[story_name]
            return jsonify(story_obj), 200
        else:
            story_names = prj.story.names
            return jsonify({'story_names': story_names}), 200

    @jwt_required()
    def post(self, project_name):
        """Create a story"""

        prj = Project(project_name)
        story_name = request.json.get('story_name', None)
        prj.story.create(story_name)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def put(self, project_name, story_name):
        """Update a story"""

        prj = Project(project_name)
        content = request.json
        new_story_name = content.pop('new_story_name', None)
        prj.story.update(story_name, new_story_name, content)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def delete(self, project_name, story_name):
        """Delete a story"""

        prj = Project(project_name)
        prj.story.delete(story_name)
        return jsonify({"msg": "OK"}), 200


def init(app: Flask):

    story_view = StoryAPI.as_view('story_api')
    app.add_url_rule('/projects/<string:project_name>/stories',
                     defaults={'story_name': None},
                     view_func=story_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/stories',
                     view_func=story_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/stories/<string:story_name>',
                     view_func=story_view,
                     methods=['GET', 'PUT', 'DELETE'])
