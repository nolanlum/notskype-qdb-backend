import connexion
import mongoengine

from qdb import models # noqa

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api.yaml')

# Expose application for uWSGI.
application = app.app

# Configure mongoengine

if __name__ == '__main__':
    app.run(port=8080, debug=True)
