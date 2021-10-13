import pandas as pd

from datetime import timedelta
from prefect import Flow, task
from prefect.executors import LocalDaskExecutor
from prefect.schedules import Schedule, clocks
from prefect.storage import GitHub


executor = LocalDaskExecutor(num_workers=4)

schedule = Schedule(
    clocks=[
        clocks.IntervalClock(timedelta(hours=4))
    ]
)

storage = GitHub(
    repo="zzstoatzz/demos",
    path="prefect/hello-prefect/flow.py",
    access_token_secret="general"
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
    "test",
    storage=storage,
    executor=LocalDaskExecutor(scheduler="threads", num_workers=1),

) as flow:

    raw_data = extract()
    data = transform(raw_data=raw_data)
    result = load(data)

if __name__ == "__main__":
    flow.run(run_on_schedule=False)