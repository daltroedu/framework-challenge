from marshmallow import fields

from app.ext.serializer.flask_marshmallow import ma


class PostImageSchema(ma.Schema):
    url = fields.Str()


class CommentSchema(ma.Schema):
    id = fields.Int()
    contents = fields.Str()


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_at', 'user_id', 'title', 'contents', 'images', 'comments')

    images = ma.Nested(PostImageSchema, many=True)
    comments = ma.Nested(CommentSchema, many=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)