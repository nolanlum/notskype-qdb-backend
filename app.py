import connexion
import mongoengine

import config
import qdb
from qdb.json import DocumentJSONEncoder

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api.yaml')

# Expose application for uWSGI.
application = app.app

# Configure mongoengine
mongoengine.register_connection(alias=mongoengine.DEFAULT_CONNECTION_NAME, host=config.MONGODB_URL)

# Provide a custom JSONEncoder to serialize our Quote model.
application.json_encoder = DocumentJSONEncoder

# Pass configuration attributes to the qdb module.
qdb.AUTH_ENABLED = config.AUTH_ENABLED
qdb.CLIENT_ID = config.CLIENT_ID
qdb.AUTHORIZED_USERS = config.AUTHORIZED_USERS


if __name__ == '__main__':
    app.run(port=8080, debug=True)
