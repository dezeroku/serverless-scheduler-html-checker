import logging
from typing import TYPE_CHECKING, Union

import botocore

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
else:
    S3Client = object

StateResponse = Union[str, None]
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_state(s3_client: S3Client, bucket_name: str, path: str) -> StateResponse:
    """
    If the temp state (HTML of a previous check) exists for an id, return it.
    Otherwise return None
    """
    logger.debug("Getting state from: %s", path)
    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=path)
    except botocore.exceptions.ClientError as exc:
        if exc.response["Error"]["Code"] == "NoSuchKey":
            logger.debug("No object found for path: %s", path)
            return None
        raise exc

    content = obj["Body"].read().decode()
    return content


def write_state(s3_client: S3Client, bucket_name: str, path: str, body: str):
    """
    Save the state in the bucket
    """
    logger.debug("Writing state to: %s", path)
    s3_client.put_object(Bucket=bucket_name, Key=path, Body=body)
