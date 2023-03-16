import json
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypy_boto3_ses import SESClient
else:
    SESClient = object

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def send_email(
    ses_client: SESClient,
    template_name: str,
    source_email: str,
    addresses: list[str],
    url: str,
):
    logger.debug("Sending change email to: %s", str(addresses))
    ses_client.send_templated_email(
        Source=source_email,
        Destination={"ToAddresses": addresses},
        Template=template_name,
        TemplateData=json.dumps(
            {
                "url": url,
            }
        ),
    )
