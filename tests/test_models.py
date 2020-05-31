import pytest
from challengeProject.models import Review, Lender


@pytest.fixture(scope='module')
def new_review():
    review = Review("TestReview", "Message Texts", "Test Author", "5 out of 5 stars", "Jan 2019", "Mortgage")
    return review
@pytest.fixture(scope='module')
def new_lender():
    lender = Lender("Test Bank")
    return lender

class TestReview:
    def test_instantiation(self, new_review):
        assert new_review.title == "TestReview"
        assert new_review.text == "Message Texts"
        assert new_review.author == "Test Author"
        assert new_review.star_rating == "5 out of 5 stars"
        assert new_review.date == "Jan 2019"
        assert new_review.loan_type == "Mortgage"
    def test_serialize(self, new_review):
        assert new_review.serialize() ==  {
            'title' : "TestReview",
            'text' : "Message Texts",
            'author' : "Test Author",
            'star_rating' : "5 out of 5 stars",
            'date' : "Jan 2019",
            'loan_type' : "Mortgage"
        }

class TestLender:
    def test_instantiation(self,new_lender):
        assert new_lender.name == "Test Bank"
        assert len(new_lender.reviews) == 0
    def test_add_review(self, new_lender, new_review):
        new_lender.add_review(new_review)
        assert len(new_lender.reviews) == 1
        assert  new_lender.reviews[0].title == "TestReview"