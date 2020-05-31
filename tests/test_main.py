
import pytest
from challengeProject import main

import flask


app = main.create_app()
app.config['TESTING'] = True
def test_context():
    with app.test_request_context('/reviews?Link=https://www.lendingtree.com/reviews/mortgage/wyndham-capital-mortgage/1127425'):
        assert flask.request.path == '/reviews'
        assert flask.request.args['Link']=='https://www.lendingtree.com/reviews/mortgage/wyndham-capital-mortgage/1127425'
def test_review_fetch():
    response = main.get_reviews_by_uri("https://www.lendingtree.com/reviews/mortgage/wyndham-capital-mortgage/1127425",'Wyndam Capital Mortgage')
    assert response.status_code == 200

