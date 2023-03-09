from mypy_boto3_s3 import S3Client

from serverless_scheduler_html_checker.bucket_state import get_state, write_state


def test_get_state_not_existing(helpers, mock_s3: S3Client, example_bucket_name):
    helpers.empty_mock_bucket(mock_s3, example_bucket_name)
    assert get_state(mock_s3, example_bucket_name, "not-existing-path") is None


def test_get_state_existing(helpers, mock_s3: S3Client, example_bucket_name):
    helpers.empty_mock_bucket(mock_s3, example_bucket_name)
    key = "test-object"
    body = "test-body"
    mock_s3.put_object(Bucket=example_bucket_name, Key=key, Body=body.encode())
    assert get_state(mock_s3, example_bucket_name, key) == body


def test_write_state_existing(helpers, mock_s3: S3Client, example_bucket_name):
    helpers.empty_mock_bucket(mock_s3, example_bucket_name)
    key = "test-object"
    body = "test-body"
    write_state(mock_s3, example_bucket_name, key, body)
    assert (
        mock_s3.get_object(Bucket=example_bucket_name, Key=key)["Body"].read().decode()
        == body
    )
