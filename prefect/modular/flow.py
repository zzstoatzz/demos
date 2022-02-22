from setup import schedule, storage

from prefect import Flow

with Flow('My Flow', schedule=schedule, storage=storage):
    pass

# prefect register -p flow.py --project my-existing-project
# above will build docker image based on Dockerfile