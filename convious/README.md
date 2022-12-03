# vote for places to lunch today

## Getting Started

### Prerequisites

* Docker Engine >= 18.06.1
* Docker Compose >= 1.24.1
* Python 3.11 (optional)
* Poetry (optional)
* Pre-commit (optional)
* GNU Make (optional)

### Setup

```bash
cp .env.example .env
# optionally edit and save .env file
make bootstrap
```

### Resetting the development database state

```bash
make reset-db
```


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
