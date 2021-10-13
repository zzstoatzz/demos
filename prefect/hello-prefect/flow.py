import pandas as pd

from prefect import Flow, task
from prefect.run_configs import DockerRun
from prefect.storage import GitHub

run_config = DockerRun(
    image='slateco/prefect-pandas-pgsql:latest'
)

storage = GitHub(
    repo="zzstoatzz/demos",
    path="prefect/hello-prefect/flow.py",
    access_token_secret="GITHUB_PAT"
)

@task(name="Extract data from somewhere")
def extract() -> dict:
    return {}

@task(name="Transform data somehow")
def transform(raw_data: dict) -> pd.DataFrame:

    # do things to do the data
    dataframe = pd.DataFrame(raw_data)

    return dataframe

@task(name="Load data to somewhere")
def load(data: pd.DataFrame) -> None:

    data.to_csv('test.csv')


with Flow(
    "My Test Flow",
    storage=storage,
    run_config=run_config

) as flow:

    raw_data = extract()
    data = transform(raw_data=raw_data)
    result = load(data)

if __name__ == "__main__":
    flow.run(run_on_schedule=False)