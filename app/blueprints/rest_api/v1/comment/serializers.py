from app.ext.serializer.flask_marshmallow import ma


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_at', 'contents', 'user_id', 'post_id')


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)