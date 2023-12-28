# Planner 5D Scraper

A homework test task.

## Task definition

Quoted from the original email

> Task: Create a small page that loads list projects from our gallery page and generates a CSV.

> 1. Open Planner 5D gallery (https://planner5d.com/gallery/floorplans) and manually select links of at least 25 projects from there (investigate page to understand how to do it)
> 2. Emit all the projects you selected in step 1. to CSV,
> 2.1. Each record should contain fields: [hash], [title], [total rooms], [total floors]
> 2.2. [total rooms] and [total floors] values should be computed dynamically by parsing project JSON (part of the task is to find this JSON)
> 2.3. Information should loaded on-the-fly and in parallel, with limit of 3 requests in parallel
> 2.4. You should write straight to CSV, without storing anything in memory - once you get information for a record you output it to CSV file

> Requirements
> Use Python
> At least 1 unit-test
> Provide task result as a git repository packaged in a gitbundle and do not post it on public code sharing services (github, bitbucket, ...)
> We expect to be able to run your code without fuss - so if there are any specifics that are needed to get your code running, please commit them to git repository if possible

> What we will look at
> Clarity, elegance and maintainability of code
> Code consistency
> A clear architecture and adherence to design patterns

> What we don't want to see
> Over engineering your code
> Fancy UI / UX


## Solution

This is a simple project implementing the above requirements.

Tech stack:

- Python 3.12
- Aiohttp
- Click

Development dependencies:

- pytest:
  - pytest-asyncio
  - aioresponses
  - faker
- pre-commit:
  - ruff
  - mypy
- pipenv


### Installation

You will need Python 3.12 and `pipenv` installed.
Navigate into the project folder and run
```bash
pipenv sync
```
to create the virtual environment and install the requirements, then
```bash
pipenv shell
```
to activate the virtual environment.

The following instructions assume you are inside `pipenv shell`.

### Usage

The provided solution supports two modes of operation: command-line and interactive (web).

#### Command-line mode
Command-line mode expects a list of project links to scrape (as a file, or piped into stdin) and outputs the scraped data in CSV format (to the specified file or stdout).

Example 1: input from stdin, output to stdout.
```bash
$ python -m p5d_scraper - - <<<EOF
https://planner5d.com/gallery/floorplans/LJZadG/floorplans-furniture-decor-living-room-lighting-3d
https://planner5d.com/gallery/floorplans/LPZaOZ/floorplans-household-kitchen-outdoor-apartment-decor-3d
EOF
hash,title,total_rooms,total_floors
3268b575782415a75ef33cbbda1e9d19,Trick or Treat : Design battle contest,1,1
3853c6582bca87372be63b23c7e78d10,wide house,19,2
```

Example 2: input from `links.txt` file, output to `gallery.csv` file.
```bash
$ python -m p5d_scraper links.txt gallery.csv
$ cat links.txt
https://planner5d.com/gallery/floorplans/LJZadG/floorplans-furniture-decor-living-room-lighting-3d
https://planner5d.com/gallery/floorplans/LPZaOZ/floorplans-household-kitchen-outdoor-apartment-decor-3d
$ cat gallery.csv
hash,title,total_rooms,total_floors
3268b575782415a75ef33cbbda1e9d19,Trick or Treat : Design battle contest,1,1
3853c6582bca87372be63b23c7e78d10,wide house,19,2
```

#### Interactive mode
Interactive mode allows the user to select the links to scrape using a simple web
interface, and returns the resulting CSV file as a download.

Example: launching in interactive mode.
```bash
$ python -m p5d_scraper --interactive
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```

Now, open `http://localhost:8080/` page in your browser.
After a short delay, you will be presented with a list of project links from the first 3
pages of the Planner 5D gallery. Select the projects to scrape by checking the
chekboxes, then submit the form by pressing Enter key or clicking the "Submit" button.
After a few seconds, a CSV file with the scraping results will be downloaded.


### Architecture

The solution consists of a single Python package, subdivided into 6 modules.

- `__main__.py`: CLI interface and general entry point.
- `models.py`: definitions of common data structures.
- `scraper.py`: scraping functions specific to Planner 5D website and API.
- `server.py`: web app implementing the Interactive mode.
- `utils.py`: self-explanatory.
- `worker.py`: concurrent scraping functions.

Additionally, the `tests` subpackage contains two test modules covering `scraper` and `worker` public functions.


### Development

Install development dependencies by running
```bash
$ pipenv sync --dev
```

Run tests with `pytest`:
```bash
$ pytest
```

Run linting, code formatting and type-checking with `pre-commit`:
```bash
$ pre-commit
```

Install `pre-commit` hooks to run `pre-commit` automatically (before each commit):
```bash
$ pre-commit install
```

Happy hacking!
