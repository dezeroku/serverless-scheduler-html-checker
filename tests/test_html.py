from serverless_scheduler_html_checker.html import generate_html_diff, get_html


def test_get_html(requests_mock, example_url):
    data = "test"
    requests_mock.get(example_url, text=data)
    assert get_html(example_url) == data


def test_generate_html_diff():
    before = "a\nb\nc"
    after = "a\nd\nb"

    assert generate_html_diff(before, after) == (
        "<p>--- previous</p></br><p>+++ current</p></br><p>@@ -1,4 +1,4 "
        + "@@</p></br><p> a</br><p>+d</br><p> b</br><p>-c</br><p> </br></p>"
    )
