# notskype QDB backend

A Python backend for the notskype QDB, backed by MongoDB.

## Development setup

1. Make sure you have Python3 and virtualenv.
1. `mkdir runtime && virtualenv runtime && . runtime/bin/activate`
1. `pip install -r requirements.txt`

## Running a development server

`$ python app.py`

A Swagger UI is available at [http://localhost:8080/api/v1/ui](http://localhost:8080/api/v1/ui).

## Running in production

Coming soon with a uWSGI near you.