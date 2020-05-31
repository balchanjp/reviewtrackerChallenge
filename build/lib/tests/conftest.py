import pytest
from challengeProject.models import Review
from challengeProject.main import create_app



@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope='module')
def new_review():
    review = Review("TestReview", "Message Texts", "Test Author", "5 out of 5 stars", "Jan 2019", "Mortgage")
    return review