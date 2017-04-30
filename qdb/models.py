from mongoengine import Document, SequenceField, StringField


class Quote(Document):
    num = SequenceField()
    author = StringField()
    body = StringField()

    @property
    def added_at(self):
        return self.id.generation_time