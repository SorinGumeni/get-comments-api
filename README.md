# Comments API

Small service which consumes a comments endpoint and returns paginated results.

## How to run locally for development

The app can be spun up locally to aid development using Docker-Compose.

### Installing Docker and docker-compose

1. Install Docker for your OS: https://docs.docker.com/get-docker/
1. Install Docker Compose: https://docs.docker.com/compose/install/
1. The instructions below assume that you have configured the docker group so that you don't have to call `sudo docker....` commands. Please change the commands appropriately if you haven't done this.

### Setup

1. Copy `./api/.env.dist` to `./api/.env`
2. Fill in the missing values if required
3. Navigate to the root directory of this repo
4. Run `docker-compose up -d` to start the stack
5. Run `docker-compose logs -f` to check for any issues

## Testing
### Run the tests
    1. Run `make build`
    2. Run `make test`

## Postman collection
    Find the attached postman collection in `test-tools` folder.

## Code formatting
### PyCharm

- Install `blackd` https://black.readthedocs.io/en/stable/blackd.html
- Run `blackd`
- Install `BlackConnect` from PyCharm plugins

### VS Code

- Install the official Python extension for VS Code
- Set `black` as the Python formatting provider in settings.
- Turn on `Editor:Format On Save` in settings

## Swagger

Swagger UI: http://localhost:8080/docs

## Packaging for deployment

- Run app `make build` or `make clean-build`