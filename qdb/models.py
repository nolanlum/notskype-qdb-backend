from mongoengine import Document, SequenceField, StringField
from json import dumps


class Quote(Document):
    meta = {
        'indexes': [
            {'fields': ['num'], 'unique': True},
            {'fields': ['$body'], 'default_language': 'english'},
            {'fields': ['author']},
        ],
    }

    num = SequenceField()
    author = StringField()
    body = StringField()

    @property
    def added_at(self):
        return self.id.generation_time

    def json(self):
        return dumps({
            'id': self.num,
            'body': self.body,
            'author': self.author,
            'addedAt': self.added_at.isoformat(),
        })
