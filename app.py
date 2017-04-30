import connexion
import mongoengine

import config

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api.yaml')

# Expose application for uWSGI.
application = app.app

# Configure mongoengine
mongoengine.register_connection(alias=mongoengine.DEFAULT_CONNECTION_NAME, host=config.MONGODB_URL)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
