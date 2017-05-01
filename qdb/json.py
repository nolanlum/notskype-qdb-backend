from connexion.apps.flask_app import FlaskJSONEncoder

from qdb.models import Quote


class DocumentJSONEncoder(FlaskJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Quote):
            return obj.json()

        # Let the base class default method raise the TypeError
        return FlaskJSONEncoder.default(self, obj)
