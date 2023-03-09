import os

import boto3
import mypy_boto3_s3
import pytest
from moto import mock_s3

_EXAMPLE_USER_EMAIL = "user@example.com"
_EXAMPLE_USER_ID = "unique-user-id"
_EXAMPLE_BUCKET_NAME = "test-bucket"


class Helpers:
    @staticmethod
    def html_monitor_job_dict_factory(
        *,
        user_email=_EXAMPLE_USER_EMAIL,
        user_id=_EXAMPLE_USER_ID,
        job_id=1,
        sleep_time=1,
        job_type="html_monitor_job",
        url="http://example.com",
        make_screenshots=False,
    ):
        return {
            "user_email": user_email,
            "user_id": user_id,
            "job_id": job_id,
            "job_type": job_type,
            "sleep_time": sleep_time,
            "url": url,
            "make_screenshots": make_screenshots,
        }

    @staticmethod
    def empty_mock_bucket(s3_client: mypy_boto3_s3.S3Client, bucket_name):
        s3_client.create_bucket(
            Bucket=bucket_name,
        )


@pytest.fixture(name="helpers")
def helpers_fixture():
    return Helpers


@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(name="example_user")
def example_user_fixture():
    return _EXAMPLE_USER_ID


@pytest.fixture(name="example_user_email")
def example_user_email_fixture():
    return _EXAMPLE_USER_EMAIL


@pytest.fixture(name="example_bucket_name")
def example_bucket_name_fixture():
    return _EXAMPLE_BUCKET_NAME


@pytest.fixture(name="mock_s3")
def mock_s3_fixture(example_bucket_name):
    with mock_s3():
        s3_client = boto3.client("s3")

        Helpers.empty_mock_bucket(s3_client, example_bucket_name)

        yield s3_client
