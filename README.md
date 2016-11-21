# sim

> Run arbitrary discrete event simulations by combining Nodes into a graph

## Requirements

1. Python 3.5

## Set up development environment

1. Install requirements
1. Install dependencies `pip install -r dependencies.txt`
1. Export environment variables:
  ```sh
  export FLASK_APP=main.py
  export FLASK_DEBUG=1
  ```

## Prepare sim's docker image for local development

1. Make sure that you have proper url information in config.ini file for development testing using container
1. Go to the app's root folder using your cli
1. Run this command to build the app's image:
  ```sh
  docker build -t divination-software/sim:dev .
  ```
1. Once you're done above step, you could continue to run the docker compose command from server app root directory

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

## Run the Server

```sh
# From the root of the repository
python setup_db.py

flask run

# Run `python sim_worker.py` ever so often via cron or similar
```
