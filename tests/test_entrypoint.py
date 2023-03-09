import os

import pytest
from common.models.plugins import parse_dict_to_job
from mypy_boto3_ses import SESClient

from serverless_scheduler_html_checker.handler import entrypoint
from tests.conftest import Helpers


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

    os.environ["BUCKET_NAME"] = example_bucket_name
    os.environ["TEMPLATE_NAME"] = example_template_name
    os.environ["SOURCE_EMAIL"] = example_source_email


@pytest.mark.parametrize(
    "event",
    [
        Helpers.sns_event_factory([]),
        Helpers.sqs_event_factory([]),
    ],
)
def test_entrypoint_no_records(
    mock_ses: SESClient,
    event,
):
    entrypoint(event, None)

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 0


@pytest.mark.parametrize(
    "event",
    [
        Helpers.sns_event_factory(
            [parse_dict_to_job(Helpers.html_monitor_job_dict_factory())]
        ),
        Helpers.sqs_event_factory(
            [parse_dict_to_job(Helpers.html_monitor_job_dict_factory())]
        ),
    ],
)
def test_entrypoint_no_previous_state(
    helpers,
    mock_ses: SESClient,
    requests_mock,
    event,
):
    job = parse_dict_to_job(helpers.html_monitor_job_dict_factory())

    data = "test"
    requests_mock.get(job.url, text=data)

    entrypoint(event, None)

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 0


@pytest.mark.parametrize(
    "event",
    [
        Helpers.sns_event_factory(
            [parse_dict_to_job(Helpers.html_monitor_job_dict_factory())]
        ),
        Helpers.sqs_event_factory(
            [parse_dict_to_job(Helpers.html_monitor_job_dict_factory())]
        ),
    ],
)
def test_entrypoint_same_previous_state(
    helpers,
    mock_ses: SESClient,
    requests_mock,
    event,
):
    job = parse_dict_to_job(helpers.html_monitor_job_dict_factory())

    data = "test"
    requests_mock.get(job.url, text=data)

    entrypoint(event, None)

    entrypoint(event, None)

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 0


@pytest.mark.parametrize(
    "event",
    [
        Helpers.sns_event_factory(
            [parse_dict_to_job(Helpers.html_monitor_job_dict_factory())]
        ),
        Helpers.sqs_event_factory(
            [parse_dict_to_job(Helpers.html_monitor_job_dict_factory())]
        ),
    ],
)
def test_entrypoint_different_previous_state(
    helpers,
    mock_ses: SESClient,
    requests_mock,
    event,
):
    job = parse_dict_to_job(helpers.html_monitor_job_dict_factory())

    data = "test"
    requests_mock.get(job.url, text=data)

    entrypoint(event, None)

    data = "test-changed"
    requests_mock.get(job.url, text=data)

    entrypoint(event, None)

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 1
