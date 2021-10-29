# Weather API

This is a simple API service providing weather forcast API.
It proxies the requests as is to Open Weather Map API, and returns the responses.

## Components

The service does not include any persistence or cache layer, and is completely stateless
and cloud-native. The only component is the Python application written in AIOHttp, run
under Gunicorn, packaged as Alpine-based Docker image.

## Configuration

The service requires a valid Open Weather Map API token to work.
You can get one for free at https://home.openweathermap.org/users/sign_up

Service configuration is done via `.env` file. To get started, copy the example end edit
it:

```bash
cp .env.example .env
```

Set the OWM API key and other parameters in the `.env` file.


## Local run

The source code includes a basic `docker-compose.yaml` configuration needed to run the
service.
To run the service, make sure to have `.env` file with the correct configuration, then
use `docker-compose up` command to build and start the service.


## Kubernetes deployment

The source code includes a basic k8s configuration needed to deploy the service into a
local `minikube` cluster. To run the service, make sure to have `.env` file configured,
then run `deploy/deploy.sh` script. It will build the image, create a `weatherapi`
namespace, a deployment, and a `NodePort` service. To test the service, you can then use

```bash
minikube kubectl --  port-forward service/weatherapi -n weatherapi 7080:8080
```
command to forward the 7080 port of your local machine to the service.


## Using the service

The service provides two endpoints:
- /token
- /weather

In order to get the weather data, first you need to call `/token` endpoint, which will
return a new JWT token. That token is required to call the `/weather` endpoint.
After aquiring the token, call `/weather` endpoint, passing the token in `Authorization: Bearer` header,
and providing a query parameter `q` with either a city name, or a `City,Country` pair.
If the token is valid, the endpoint will pass the query as is to the OWM API, and return
the response.

### /token

Method: GET
Path params: no
Query params: no
Authorization: no

This endpoint returns a new JWT token when called. It takes no parameters.
Note: It is currently impossible to revoke and individual token. All the previously issued
tokens can be invalidated at once by changing either one of `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_AUDIENCE`
or `JWT_ISSUER` configuration parameters and restarting the service.

> Possible future improvement: some sort of ACL. Possibly, accept login+password pairs or
> HTTP Basic auth, check against a list of allowed logins, and only issue a token if there
> is a match.

### /weather

This endpoint returns a weather data from the OWM API.

Method: GET
Path params: no
Query params:
  - `q` (*Required*): a city name (i.e. `?q=Vilnius`) or a city name and a country code separated by comma (i.e. `q=Vilnius,LT`)

Authorization: required, Bearer token issued by `/token` endpoint.

> Possible future improvement: call multiple weather API providers, normalize query and
> response formats, keep track of usage limits and intelligently call different providers
> based on the remaining limits and/or response time.

> Possible future improvement: caching. Store the response in cache and serve the next
> for the same location from cache instead of calling the provider API. Invalidate cache
> entries after X minutes (configurable).


## Development

This project uses Poetry for package management, pre-commit for running code quality
tooks.

To install Poetry, refer to https://python-poetry.org/docs/#installation

To bootstrap the project, use

```bash
poetry install
pre-commit install
```
