from flask import abort, jsonify, request, make_response

from flask_jwt_extended import jwt_required, get_jwt_identity

from app import photos
from app.blueprints.models import Post, PostImage
from app.blueprints.rest_api.utils import error_response, pagination
from app.blueprints.rest_api.v1 import rest_api_v1
from app.blueprints.rest_api.v1.post.serializers import post_schema, posts_schema
from app.ext.database.flask_sqlalchemy import db


@rest_api_v1.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    result = post_schema.dump(post)
    return jsonify(result), 200


@rest_api_v1.route('/posts', methods=['GET'])
def get_all_posts():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = pagination(Post.query, result, page, per_page, 'rest_api_v1.get_all_posts')
    return jsonify(data), 200


@rest_api_v1.route('/posts', methods=['POST'])
@jwt_required
def create_post():
    user_id = get_jwt_identity()
    title = request.form['title']
    contents = request.form['contents']

    post = Post(user_id, title, contents)
    post.images = []
    for p in request.files.getlist('photos'):
        filename = photos.save(p)
        img_url = photos.url(filename)
        image = PostImage(filename, img_url)
        post.images.append(image)

    try:
        db.session.add(post)
        db.session.commit()
        result = post_schema.dump(post)
        return jsonify(result), 201
    except BaseException as e:
        db.session().rollback()
        return jsonify({'message': 'unable to create'}), 500


@rest_api_v1.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required
def delete_post(id):
    post = Post.query.get_or_404(id)

    if post.user_id != get_jwt_identity():
        abort(403)

    db.session.delete(post)
    db.session.commit()

    return make_response('', 204)