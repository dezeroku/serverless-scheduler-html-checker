from serverless_scheduler_html_checker.html import get_html


def test_get_html(requests_mock, example_url):
    data = "test"
    requests_mock.get(example_url, text=data)
    assert get_html(example_url) == data
