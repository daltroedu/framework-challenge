from marshmallow import fields

from app.ext.serializer.flask_marshmallow import ma


class AlbumImageSchema(ma.Schema):
    url = fields.Str()


class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_at', 'user_id', 'title', 'contents', 'images')

    images = ma.Nested(AlbumImageSchema, many=True)


album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)