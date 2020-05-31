def test_new_review(new_review):
    assert new_review.title == "TestReview"
    assert new_review.text == "Message Texts"
    assert new_review.author == "Test Author"
    assert new_review.star_rating == "5 out of 5 stars"
    assert new_review.date == "Jan 2019"
    assert new_review.loan_type == "Mortgage"