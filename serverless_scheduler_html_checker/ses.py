import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypy_boto3_ses import SESClient
else:
    SESClient = object


def send_email(
    ses_client: SESClient,
    template_name: str,
    source_email: str,
    addresses: list[str],
    url: str,
):
    ses_client.send_templated_email(
        Source=source_email,
        Destination={"ToAddresses": addresses},
        Template=template_name,
        TemplateData=json.dumps(
            [
                {
                    "Name": "url",
                    "Value": url,
                }
            ]
        ),
    )
