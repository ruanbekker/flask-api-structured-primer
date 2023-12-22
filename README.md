# flask-api-structured-primer
Structured Flask API with SQLAlchemy, Swagger, Unit Tests, CodeCoverage, etc

## Table of Contents

- [Getting Started](#getting-started)
- [Directory Structure](#directory-structure)
- [Tests](#tests)
  - [Static Code Analysis](#static-code-analysis)
  - [Unit Tests](#unit-tests)
  - [Code Coverage](#code-coverage)
  - [Running tests with Docker](#running-tests-with-docker)
- [Database Migrations](#database-migrations)

## Getting started

To view the makefile targets:

```bash
make
```

Local testing:

```bash
make test
```

Docker:

```bash
make up
```

Scripts is under `_scripts/` or you can use the makefile targets:

```bash
make requests-create
make requests-retrieve
```

## Directory Structure

<details>
  <summary>Tree view of the directory structure:</summary>

```bash
├── Dockerfile
├── Makefile
├── README.md
├── _scripts
│   ├── http
│   │   ├── create.sh
│   │   ├── delete.sh
│   │   ├── get.sh
│   │   ├── list.sh
│   │   └── update.sh
│   ├── migrations
│   │   └── db_migrations.sh
│   └── tests
│       ├── lint.sh
│       └── unit_tests.sh
├── app.py
├── config.py
├── database
│   └── db.py
├── docker-compose.yaml
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── models
│   └── product.py
├── requirements.txt
├── services
│   └── product_service.py
├── shared
│   └── logging_utils.py
├── tests
│   └── test_product_service.py
└── views
    └── product_views.py

12 directories, 25 files
```

</details>

## Tests

- static code analysis (pylint, prospector, bandit)
- unit tests (unittest)
- code coverage (coverage)
- optional: using docker to run all at once

### Static Code Analysis

To run linting:

```bash
find . -name "*.py" ! -path "./venv/*" -exec pylint --rcfile .pylintrc --verbose {} +
```

<details>
  <summary>pylint output</summary>

```bash
Using config file .pylintrc
************* Module shared.logging_utils
shared/logging_utils.py:58:17: C0303: Trailing whitespace (trailing-whitespace)
shared/logging_utils.py:48:4: C0103: Variable name "ch" doesn't conform to snake_case naming style (invalid-name)
************* Module views.product_views
views/product_views.py:68:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
views/product_views.py:88:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)

-------------------------------------------------------------------
Your code has been rated at 9.86/10 (previous run: 10.00/10, -0.14)
```

When the issues has been fixed:

```bash
-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 9.81/10, +0.19)
```
</details>

Run prospector:

```bash
prospector --profile .prospector.yaml
# prospector --strictness low --with-tool pydocstyle
```

<details>
  <summary>prospector output</summary>

```bash
Check Information
=================
         Started: 2023-11-19 16:07:29.863667
        Finished: 2023-11-19 16:07:44.618042
      Time Taken: 14.75 seconds
       Formatter: grouped
        Profiles: .prospector.yaml, doc_warnings, strictness_medium, strictness_high, strictness_veryhigh, no_member_warnings
      Strictness: from profile
  Libraries Used: flask
       Tools Run: dodgy, profile-validator, pycodestyle, pydocstyle, pyflakes, pylint
  Messages Found: 0
 External Config: pylint: /Users/ruan/personal/eng-python-fastapi-products/.pylintrc
```

When you have errors:

```bash
Messages
========

app.py
  Line: 12
    pydocstyle: D212 / Multi-line docstring summary should start at the first line
    pydocstyle: D407 / Missing dashed underline after section ('Parameters')
    pydocstyle: D406 / Section name should end with a newline ('Parameters', not 'Parameters:')
    pydocstyle: D417 / Missing argument descriptions in the docstring (argument(s) config_class are missing descriptions in 'create_app' docstring)
    pydocstyle: D413 / Missing blank line after last section ('Returns')
    pydocstyle: D407 / Missing dashed underline after section ('Returns')
    pydocstyle: D406 / Section name should end with a newline ('Returns', not 'Returns:')
```

</details>

Run bandit security tests:

```bash
bandit -r . -ll -x ./venv
```

<details>
  <summary>bandit output</summary>

```bash
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    running on Python 3.8.18
Run started:2023-11-18 17:10:55.851705

Test results:
        No issues identified.

Code scanned:
        Total lines of code: 430
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):
```

</details>


### Unit Tests

Run unit tests:

```bash
python3 -m unittest discover -s tests --verbose
```

<details>
  <summary>unittest output</summary>

```bash
test_product_model (test_product_service.ProductModelTestCase)
Test the behavior of the Product model. ... ok
test_add_product_service (test_product_service.ProductServiceLayerTestCase)
Test the 'add_product' method of the ProductService class. ... ok
test_delete_product (test_product_service.ProductServiceTestCase)
Test the deletion of a product via the API. ... 2023-11-18 19:12:26,697 - views.product_views - INFO - creating a new product
2023-11-18 19:12:26,710 - views.product_views - INFO - product was deleted: product_id=1
ok
test_product_creation (test_product_service.ProductServiceTestCase)
Test the creation of a product via the API. ... 2023-11-18 19:12:26,720 - views.product_views - INFO - creating a new product
ok
test_product_retrieval (test_product_service.ProductServiceTestCase)
Test the retrieval of a product via the API. ... 2023-11-18 19:12:26,740 - views.product_views - INFO - retrieving details for product id=1
ok
test_update_product (test_product_service.ProductServiceTestCase)
Test the updating of a product via the API. ... 2023-11-18 19:12:26,750 - views.product_views - INFO - creating a new product
2023-11-18 19:12:26,759 - views.product_views - INFO - updating product details for product id=1
ok

----------------------------------------------------------------------
Ran 6 tests in 0.121s

OK
```

</details>


### Code Coverage

Run code coverage:

```bash
coverage run --rcfile .coveragerc -m unittest discover -s tests 
```

<details>
  <summary>coverage output</summary>

```bash
..2023-11-18 19:13:21,309 - views.product_views - INFO - creating a new product
2023-11-18 19:13:21,327 - views.product_views - INFO - product was deleted: product_id=1
.2023-11-18 19:13:21,344 - views.product_views - INFO - creating a new product
.2023-11-18 19:13:21,371 - views.product_views - INFO - retrieving details for product id=1
.2023-11-18 19:13:21,385 - views.product_views - INFO - creating a new product
2023-11-18 19:13:21,398 - views.product_views - INFO - updating product details for product id=1
.
----------------------------------------------------------------------
Ran 6 tests in 0.161s

OK
```

</details>

Run the coverage report:

```bash
coverage report --rcfile .coveragerc
```

<details>
  <summary>coverage report output</summary>

```bash
Name                            Stmts   Miss  Cover
---------------------------------------------------
app.py                             17      0   100%
config.py                           8      0   100%
database/db.py                      5      2    60%
models/product.py                  11      1    91%
services/product_service.py        35      3    91%
shared/logging_utils.py            19      1    95%
tests/test_product_service.py      85      1    99%
views/product_views.py             40      8    80%
---------------------------------------------------
TOTAL                             220     16    93%
```

</details>

### Running tests with docker

Tests can be run as instructed above or can be run all at once using docker:

```bash
make test-docker
```

## Database Migrations

This application uses the [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) extension for a [Alembic](https://alembic.sqlalchemy.org/en/latest/) migration environment.

<details>
  <summary>To run database migrations:</summary>

Setting the environment:

```bash
export FLASK_APP=app:create_app
export FLASK_ENV=development
```

Running the database migrations

```bash
flask db init
flask db migrate -m "Initial db migration"
flask db upgrade
```

The database versioning directory structure:

```bash
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── models
│   └── product.py
```

</details>

Resources:
- [Database Migrations with Flask](https://code.likeagirl.io/database-migrations-in-python-with-flask-with-alembic-442d11eb14d3)
