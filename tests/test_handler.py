import pytest
from common.models.plugins import parse_dict_to_job
from mypy_boto3_s3 import S3Client
from mypy_boto3_ses import SESClient

from serverless_scheduler_html_checker.handler import handler


@pytest.fixture(autouse=True)
def common_setup(
    helpers,
    mock_s3,
    mock_ses,
    example_bucket_name,
    example_template_name,
    example_source_email,
):
    helpers.empty_mock_bucket(mock_s3, example_bucket_name)
    helpers.create_ses_template(mock_ses, example_template_name)
    helpers.verify_ses_email(mock_ses, example_source_email)


def test_handler_no_records(
    mock_s3: S3Client,
    mock_ses: SESClient,
    example_bucket_name,
    example_template_name,
    example_source_email,
):
    handler(
        [],
        mock_s3,
        example_bucket_name,
        mock_ses,
        example_template_name,
        example_source_email,
    )

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 0


def test_handler_no_previous_state(
    helpers,
    mock_s3: S3Client,
    mock_ses: SESClient,
    example_bucket_name,
    example_template_name,
    example_source_email,
    requests_mock,
):
    job = parse_dict_to_job(helpers.html_monitor_job_dict_factory())

    data = "test"
    requests_mock.get(job.url, text=data)

    handler(
        [job],
        mock_s3,
        example_bucket_name,
        mock_ses,
        example_template_name,
        example_source_email,
    )

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 0


def test_handler_same_previous_state(
    helpers,
    mock_s3: S3Client,
    mock_ses: SESClient,
    example_bucket_name,
    example_template_name,
    example_source_email,
    requests_mock,
):
    job = parse_dict_to_job(helpers.html_monitor_job_dict_factory())

    data = "test"
    requests_mock.get(job.url, text=data)

    handler(
        [job],
        mock_s3,
        example_bucket_name,
        mock_ses,
        example_template_name,
        example_source_email,
    )

    handler(
        [job],
        mock_s3,
        example_bucket_name,
        mock_ses,
        example_template_name,
        example_source_email,
    )

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 0


def test_handler_different_previous_state(
    helpers,
    mock_s3: S3Client,
    mock_ses: SESClient,
    example_bucket_name,
    example_template_name,
    example_source_email,
    requests_mock,
):
    job = parse_dict_to_job(helpers.html_monitor_job_dict_factory())

    data = "test"
    requests_mock.get(job.url, text=data)

    handler(
        [job],
        mock_s3,
        example_bucket_name,
        mock_ses,
        example_template_name,
        example_source_email,
    )

    data = "test-changed"
    requests_mock.get(job.url, text=data)

    handler(
        [job],
        mock_s3,
        example_bucket_name,
        mock_ses,
        example_template_name,
        example_source_email,
    )

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 1
