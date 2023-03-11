import json
import logging
import os
from typing import TYPE_CHECKING

import boto3
from common.models.plugins import parse_dict_to_job
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def entrypoint(event, context):
    # pylint: disable=unused-argument
    s3_client = boto3.client("s3")
    bucket_name = os.environ["BUCKET_NAME"]
    ses_client = boto3.client("ses")
    template_name = os.environ["TEMPLATE_NAME"]
    source_email = os.environ["SOURCE_EMAIL"]

    # The event can come either from SNS (direct connection)
    # or SQS (if it's defined as a buffer)
    # Therefore get the job definitions out of the event
    # and pass them to the handler in a unified format
    if records := event.get("Records"):
        logger.debug(records)
        if "Sns" in records[0]:
            to_use = map(lambda x: x["Sns"]["Message"], records)
        else:
            to_use = map(lambda x: x["body"], records)

        to_use_records = map(lambda x: parse_dict_to_job(json.loads(x)), to_use)

        handler(
            to_use_records,
            s3_client,
            bucket_name,
            ses_client,
            template_name,
            source_email,
        )


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
