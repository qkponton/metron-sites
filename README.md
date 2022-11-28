# metron-sites

## Usage
To run the server, please execute the following from the root directory:

### ENVIRONMENT VARIABLES
```shell
DB_USER=
DB_PWD=
DB_NAME=
DB_HOST=0.0.0.0
```

### RUN WITH DOCKER
```shell
docker-compose up
```

### Manual
```
pip3 install poetry
poetry install
poetry run python -m metron_sites
```

and open your browser to here:

```
http://localhost:8000/
```

Your Swagger definition lives here:

```
http://localhost:8000/api/v3/swagger.json
```
