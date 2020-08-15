from app.ext.serializer.flask_marshmallow import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_at', 'email', 'username', 'name')


user_schema = UserSchema()
users_schema = UserSchema(many=True)