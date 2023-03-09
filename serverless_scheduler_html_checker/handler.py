from typing import TYPE_CHECKING

from serverless_scheduler_html_checker_api.models.html_monitor_job import HTMLMonitorJob

from serverless_scheduler_html_checker.bucket_state import get_state, write_state
from serverless_scheduler_html_checker.html import get_html
from serverless_scheduler_html_checker.ses import send_email

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_ses import SESClient
else:
    S3Client = object
    SESClient = object


def entrypoint(event, context):
    # pylint: disable=unused-argument
    pass


def handler(
    records: list[HTMLMonitorJob],
    s3_client: S3Client,
    bucket_name: str,
    ses_client: SESClient,
    template_name: str,
    source_email: str,
):
    for rec in records:
        state = get_html(rec.url)
        path = rec.get_unique_job_id()
        if (old_state := get_state(s3_client, bucket_name, path)) is not None:
            if state != old_state:
                send_email(
                    ses_client, template_name, source_email, [rec.user_email], rec.url
                )

        write_state(s3_client, bucket_name, path, state)
