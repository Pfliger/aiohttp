from datetime import datetime
from asyncpg import UniqueViolationError
from aiohttp import web
import hashlib
from gino import Gino



db = Gino()

class BaseModel:

    @classmethod
    async def get_or_404(cls, id):
        instance = await cls.get(id)
        if instance:
            return instance
        raise web.HTTPNotFound()

    @classmethod
    async def delete_or_404(cls, id):
        instance = await cls.get(id)
        if instance:
            await instance.delete()
            return id
        raise web.HTTPNotFound()

    @classmethod
    async def create_instance(cls, **kwargs):
        try:
            instance = await cls.create(**kwargs)
        except UniqueViolationError:
            raise web.HTTPBadRequest()
        return instance

class User(db.Model, BaseModel):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))

    def to_dict(self):
        dict_user = super().to_dict()
        dict_user.pop("password")
        return dict_user

    @classmethod
    async def create_instance(cls, **kwargs):
        kwargs['password'] = hashlib.md5(kwargs['password'].encode()).hexdigest()
        return await super().create_instance(**kwargs)


class Post(db.Model, BaseModel):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.String(1000))
    created_date = db.Column(db.String(50), default=datetime.isoformat(datetime.utcnow()))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def to_dict(self):
        posts = {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "created_date": str(self.created_date),
            "user_id": self.user_id
        }
        return posts
