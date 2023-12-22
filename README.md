# flask-api-structured-primer
Structured Flask API with SQLAlchemy, Swagger, Unit Tests, CodeCoverage, etc

## Getting Started

Local testing:

```bash
make test
```

Docker:

```bash
docker compose up --build -d
```

Scripts is under `_scripts/`

## Directory Structure

This is the directory structure:

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
├── models
│   └── product.py
├── requirements.txt
├── services
│   └── product_service.py
├── tests
│   └── test_product_service.py
└── views
    └── product_views.py

9 directories, 20 files
```