from mypy_boto3_ses import SESClient

from serverless_scheduler_html_checker.ses import send_email


def test_send_email(
    helpers,
    mock_ses: SESClient,
    example_template_name,
    example_source_email,
    example_target_addresses,
    example_url,
):
    helpers.create_ses_template(mock_ses, example_template_name)
    helpers.verify_ses_email(mock_ses, example_source_email)

    send_email(
        mock_ses,
        example_template_name,
        example_source_email,
        example_target_addresses,
        example_url,
    )

    assert int(mock_ses.get_send_quota()["SentLast24Hours"]) == 1
