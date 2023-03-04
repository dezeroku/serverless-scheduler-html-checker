from common.models.jobs import ScheduledJob
from pydantic import HttpUrl, validator


class HTMLMonitorJob(ScheduledJob):
    make_screenshots: bool = False
    url: HttpUrl

    @validator("job_type")
    def validate_job_type(cls, v):
        # pylint: disable=no-self-argument,invalid-name
        expected = "html_monitor_job"
        if v.value != expected:
            raise ValueError(
                f"Incorrect job_type provided: '{v.value}' instead of '{expected}'"
            )

        return v
