from flaskygram.database import db, BaseMixin


class Tag(db.Model, BaseMixin):
    __tablename__ = 'tags'