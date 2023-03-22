import json
import logging
from typing import TYPE_CHECKING

import botocore

if TYPE_CHECKING:
    from mypy_boto3_ses import SESClient
else:
    SESClient = object

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _send_email(
    ses_client: SESClient,
    template_name: str,
    source_email: str,
    addresses: list[str],
    url: str,
    diff_html: str,
):
    ses_client.send_templated_email(
        Source=source_email,
        Destination={"ToAddresses": addresses},
        Template=template_name,
        TemplateData=json.dumps(
            {
                "url": url,
                "diff_html": diff_html,
            }
        ),
    )


def send_email(
    ses_client: SESClient,
    template_name: str,
    source_email: str,
    addresses: list[str],
    url: str,
    diff_html: str,
):
    logger.debug("Sending change email to: %s", str(addresses))
    try:
        _send_email(ses_client, template_name, source_email, addresses, url, diff_html)
    except botocore.exceptions.ClientError as exc:
        if exc.response["Error"]["Code"] == "ValidationError":
            logger.warning("Could not send email, trying with empty diff")
            _send_email(
                ses_client,
                template_name,
                source_email,
                addresses,
                url,
                "Too long diff to attach",
            )
        else:
            raise exc
