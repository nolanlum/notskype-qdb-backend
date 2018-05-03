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
qdb.CLIENT_SECRET = config.CLIENT_SECRET
qdb.SLACK_TEAM_ID = config.SLACK_TEAM_ID
qdb.SECRET_KEY = config.SECRET_KEY

@app.app.route('/api/healthcheck')
def healthcheck():
    response = app.app.make_response('ok')
    response.mimetype = 'text/plain'
    return response

if __name__ == '__main__':
    app.run(port=8080, debug=True)
