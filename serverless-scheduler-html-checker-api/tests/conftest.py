import pytest

_EXAMPLE_USER_EMAIL = "user@example.com"
_EXAMPLE_USER_ID = "unique-user-id"


class Helpers:
    @staticmethod
    def html_monitor_job_dict_factory(
        *,
        user_email=_EXAMPLE_USER_EMAIL,
        user_id=_EXAMPLE_USER_ID,
        job_id=1,
        make_screenshots=True,
        sleep_time=1,
        url="http://example.com",
        job_type="html_monitor_job",
    ):
        return {
            "user_email": user_email,
            "user_id": user_id,
            "job_id": job_id,
            "make_screenshots": make_screenshots,
            "sleep_time": sleep_time,
            "url": url,
            "job_type": job_type,
        }


@pytest.fixture(name="helpers")
def helpers_fixture():
    return Helpers


@pytest.fixture()
def example_user_email():
    return _EXAMPLE_USER_EMAIL


@pytest.fixture()
def example_user_id():
    return _EXAMPLE_USER_ID
