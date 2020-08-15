from flask import abort, jsonify, request, make_response

from flask_jwt_extended import jwt_required, get_jwt_identity

from app.blueprints.models import Comment
from app.blueprints.rest_api.utils import error_response, pagination
from app.blueprints.rest_api.v1 import rest_api_v1
from app.blueprints.rest_api.v1.comment.serializers import comment_schema, comments_schema
from app.ext.database.flask_sqlalchemy import db


@rest_api_v1.route('/comments/<int:id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    result = comment_schema.dump(comment)
    return jsonify(result), 200


@rest_api_v1.route('/comments', methods=['GET'])
def get_all_comments():
    all_comments = Comment.query.all()
    result = comments_schema.dump(all_comments)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = pagination(Comment.query, result, page, per_page, 'rest_api_v1.get_all_comments')
    return jsonify(data), 200


@rest_api_v1.route('/comments', methods=['POST'])
@jwt_required
def create_comment():
    data = request.get_json() or {}

    user_id = get_jwt_identity()
    post_id = data['post_id']
    contents = data['contents']
    
    comment = Comment(user_id, post_id, contents)

    try:
        db.session.add(comment)
        db.session.commit()
        result = comment_schema.dump(comment)
        return jsonify(result), 201
    except BaseException as e:
        db.session().rollback()
        return jsonify({'message': 'unable to create'}), 500


@rest_api_v1.route('/comments/<int:id>', methods=['DELETE'])
@jwt_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)

    if comment.user_id != get_jwt_identity():
        abort(403)

    db.session.delete(comment)
    db.session.commit()

    return make_response('', 204)