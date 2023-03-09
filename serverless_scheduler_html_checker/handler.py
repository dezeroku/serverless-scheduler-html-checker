from typing import TYPE_CHECKING

from serverless_scheduler_html_checker_api.models.html_monitor_job import HTMLMonitorJob

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_ses import SESClient
else:
    S3Client = object
    SESClient = object


def entrypoint(event, context):
    # pylint: disable=unused-argument
    pass


def handler(records: list[HTMLMonitorJob], s3_client: S3Client, ses_client: SESClient):
    pass
