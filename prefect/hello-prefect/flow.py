import asyncio
import pandas as pd
import requests
import sys
from prefect import context, Flow, Parameter, task
from prefect.run_configs import DockerRun
from prefect.storage import GitHub

logger = context.get("logger")

run_config = DockerRun(
    image='slateco/prefect-pandas-pgsql:latest'
)

storage = GitHub(
    repo="zzstoatzz/demos",
    path="prefect/hello-prefect/flow.py",
    access_token_secret="GITHUB_PAT"
)

async def get_cat_fact() -> dict:
    URL = "https://catfact.ninja/fact"
    HEADERS = {"accept": "application/json"}
    response = requests.get(
        url=URL,
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()

@task(name="Get something from somewhere")
def extract(N: int) -> dict:
    loop = asyncio.get_event_loop()
    items = asyncio.gather(*[get_cat_fact() for i in range(N)])
    results = loop.run_until_complete(items)
    return results

@task(name="Transform data somehow")
def transform(raw_data: dict) -> pd.DataFrame:
    return pd.DataFrame(raw_data)

@task(name="Load data to somewhere")
def load(data: pd.DataFrame) -> None:
    data.to_csv('cat_facts.csv', index=False)
    logger.info(f"There are {sum(data['length'])} characters in {data.shape[0]} cat fact(s)")

with Flow(
    "My Test Flow",
    storage=storage,
    run_config=run_config

) as flow:
    some_number_of_cat_facts = Parameter(
        "some_number_of_cat_facts", default=1
    )

    raw_data = extract(some_number_of_cat_facts)
    data = transform(raw_data=raw_data)
    result = load(data)

if __name__ == "__main__":
    try:
        N = sys.argv[1]
    except IndexError:
        N = 1

    params = dict(
        some_number_of_cat_facts = int(N)
    )

    flow.run(parameters=params)