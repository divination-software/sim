# sim

> Some description

## Requirements

1. Python 3.5

## Set up development environment

1. Install requirements
1. Install dependencies `pip install -r dependencies.txt`
1. Export environment variables:
  ```sh
  export FLASK_APP=server.py
  export FLASK_DEBUG=1
  ```

## Run Tests

```sh
# From the root of the repository
python -m unittest
```

## Run Lint

```sh
# From the root of the repository
python run_pylint.py
```

## Start server

```sh
# From the root of the repository
flask run
```
