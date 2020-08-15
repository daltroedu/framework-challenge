from flask import abort, jsonify, request, make_response

from flask_jwt_extended import jwt_required, get_jwt_identity

from app import photos
from app.blueprints.models import Album, AlbumImage
from app.blueprints.rest_api.utils import error_response, pagination
from app.blueprints.rest_api.v1 import rest_api_v1
from app.blueprints.rest_api.v1.album.serializers import album_schema, albums_schema
from app.ext.database.flask_sqlalchemy import db


@rest_api_v1.route('/albums/<int:id>', methods=['GET'])
def get_album(id):
    album = Album.query.get_or_404(id)
    result = album_schema.dump(album)
    return jsonify(result), 200


@rest_api_v1.route('/albums', methods=['GET'])
def get_all_albums():
    all_albums = Album.query.all()
    result = albums_schema.dump(all_albums)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = pagination(Album.query, result, page, per_page, 'rest_api_v1.get_all_albums')
    return jsonify(data), 200


@rest_api_v1.route('/albums', methods=['POST'])
@jwt_required
def create_album():
    user_id = get_jwt_identity()
    title = request.form['title']
    contents = request.form['contents']

    album = Album(user_id, title, contents)
    album.images = []
    for p in request.files.getlist('photos'):
        filename = photos.save(p)
        img_url = photos.url(filename)
        image = AlbumImage(filename, img_url)
        album.images.append(image)

    try:
        db.session.add(album)
        db.session.commit()
        result = album_schema.dump(album)
        return jsonify(result), 201
    except BaseException as e:
        db.session().rollback()
        return jsonify({'message': 'unable to create'}), 500


@rest_api_v1.route('/albums/<int:id>', methods=['DELETE'])
@jwt_required
def delete_album(id):
    album = Album.query.get_or_404(id)

    if album.user_id != get_jwt_identity():
        abort(403)

    db.session.delete(album)
    db.session.commit()

    return make_response('', 204)