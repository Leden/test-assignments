# vote for places to lunch today

## Note for reviewers

Dear reviewer, thank you for finding time to look at this repo.
In front of you lies the result of several days of my work.
I hope you will find my solution acceptable, and enjoy reading this code as
much as I have enjoyed writing it.


## Architecture and code layout overview

Tech stack used: Python 3.11, Django 3.2 LTS, GraphQL, VanillaJS, PostgreSQL.
Tests: pytest, factory-boy.

The `backend/` folder contains the Python/Django code as well as Poetry and Docker
configuration files.

Django apps are nested inside of the project package because such
layout simplifies Poetry configuraion: is only needs to build and install a single
Python package, instead of having a separate package for each app.

- `api` app contains GraphQL API definition code.
- `home` app contains the index page with a simple frontend app utilizing the API.
- `lib` is not a Django app, but a small utility package.
- `restaurants` app contains the Restaurant model and related business logic.
- `users` app contains the custom User model and related business logic.
- `votes` app contains the Vote model and related business logic.

This project follows neither "fat models" nor "fat views" approach. Instead, it
attempts to contain the business logic in its own layer. The corresponding code
can be found in `services` module inside of each app. In my experience, such
layout has proven to be more scalable for big projects, than the other two mentioned.

It is also worth mentioning that some of the dependency packages (i.e. Celery) or utilities in `lib`
are not used. This is due to the fact that this project was bootstrapped from the
cookiecutter template I'm using in most of my production projects, which contains the
generic set of most frequently used tools.


## Getting Started

### Prerequisites

The following tools must be present on your host machine to run this code in developer
mode:

* Docker Engine >= 18.06.1
* Docker Compose >= 1.24.1

The following tools are recommended to have on your host machine, but not strictly
required:

* Python 3.11
* GNU Make 4.1+
* Poetry (automatically installed by bootstrapping script)
* Pre-commit (automatically installed by bootstrapping script)

### Setup

First, clone the repo and `cd` into the created folder.
Then, prepare the `.env` file by copying the provided example.

```bash
cp .env.example .env
```

Open the created `.env` file and adjust the values if necessary.
The default values should be enough to get started.

If you have `make` utility instaled (specifically, GNU Make!), you can run

```bash
make bootstrap
```

to launch the bootstrapping script which will attempt to verify the installed versions
of Docker, Docker Compose, Python, Make; install Poetry and Pre-commit, and start the
Docker image build process. This is optional, however, and you can do all of that
manually.

After successfully building the Docker image, run `make reset-db start` to create the database and start the service.
Verify everything is working by visiting `http://localhost:8000`.


### Demo frontend app

You should see the minimalistic UI demonstrating (some of) the functionality provided by
the API at the index page.

Enter the built-in `root:root` user credentials into the input fields on the top and
click the "Login" button. The UI will refresh and allow you to cast votes for one of the
restaurants below by clicking "Vote" buttons next to the selected restaurant, in the
Today section.

After casting each vote, UI will refresh and sort the list of restaurants based on their
current votes, with the winner on top. After casting the allowed number of votes, new
votes from the same user on the same day will be rejected, and an error will be
displayed at the bottom of the page. Possible improvement for the future: allow to query
the total and used-up votes per user, and change the UI to reflect the fact that the user
has used up all the votes for today.

The History section below the Today section displays the results of the votes happened
over the previous 7 days. Visit again tomorrow and DO NOT reset the database :D

The source code of the frontend app is located in `backend/lunchvote/home/templates/home/index.html`.
It can be used as an example of how to use the GraphQL API.
This app is for demonstrative purposes only and should not be used in production environment.


### GraphiQL

Start the service and visit `http://localhost:8000/api/graphql` in your web browser.
You will find the built-in GraphQL sandbox called GraphiQL. It allows to explore the API
schema, write and execute queries and mutations.


### Useful `make` commands
- `make build` stops the server and rebuilds the Docker image. Do this after
    adding/removing/updating a Python dependency (via `poetry add` or by editing `pyproject.toml`)
- `make start` starts the server in Docker. Does not rebuild the image!
- `make stop` stops all running Docker containers.
- `make reset-db` drops and recreates the local database. Migrations and `initial_data`
    fixtures are applied automatically.
- `make test` runs the unittests.
- `make bash` runs bash inside of a new Docker container.
- `make shell` runs python shell in the pjoject environment inside of a new Docker
    container.


### Poetry

This project uses [poetry package manager](https://python-poetry.org/).

To install it, run the following in your terminal (or visit the link above for more options):

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

To add a dependency, use `poetry add [--dev] <package-name>[=<version>]`.


### Pre-commit

This project uses [pre-commit](https://pre-commit.com/) for running code quality tools.

Install it with `pip`:

```bash
pip install pre-commit
```

or with `brew`:

```bash
brew install pre-commit
```

or visit the link above for more installation options.

After installing, run `pre-commit install` to register the git hooks.
Each time you attempt to commit anything, `pre-commit` will run the code formatters and linters,
and abort the commit in case there are any errors. Fix the reported issues, add the changes and commit again.

To run the checks and formatters without committing, run `pre-commit`.


### Backend unittests: pytest

To run the backend unittests, use `make test` command. Alternatively, you can run `pytest` command directly inside of the running backend container:

```bash
make bash

pytest
```
