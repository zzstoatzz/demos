from datetime import timedelta
from prefect.executors import LocalDaskExecutor
from prefect.schedules import Schedule, clocks
from prefect.storage import Docker

executor = LocalDaskExecutor(scheduler="threads", num_workers=2)

schedule = Schedule(clocks=[clocks.IntervalClock(timedelta(days=1))])

storage = Docker(
    dockerfile="Dockerfile",
    python_dependencies=[
        "snowflake-sqlalchemy==1.3.1",
    ],
    registry_url="your_registry_url",
)