import pandas as pd

from datetime import timedelta
from prefect import Flow, task
from prefect.schedules import Schedule, clocks
from prefect.storage import GitHub


schedule = Schedule(
    clocks=[
        clocks.IntervalClock(timedelta(hours=4))
    ]
)

storage = GitHub(
    repo="zzstoatzz/demos",
    path="prefect/hello-prefect/flow.py",
    access_token_secret="GITHUB_ACCESS_TOKEN"
)

@task(name="Extract data from somewhere")
def extract() -> dict:
    pass

@task(name="Transform data somehow")
def transform() -> pd.DataFrame:
    pass

@task(name="Load data to somewhere")
def load() -> None:
    pass


with Flow("test") as flow:
    data = extract()
    transformed_data = transform(data)
    result = load(data)

if __name__ == "__main__":
    flow.run(run_on_schedule=False)