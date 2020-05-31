import pytest
from challengeProject.controller import MainController
from challengeProject.models import ExceptionResponse
import challengeProject.main as main
import json
import requests


class TestController:
    app = main.create_app()
    app.config['TESTING'] = True
    ctx = app.app_context()
    ctx.push()
    controller = MainController(app)

    def test_review_fetch(self):
        response = self.controller.get_reviews_by_uri(
            "https://www.lendingtree.com/reviews/mortgage/wyndham-capital-mortgage/1127425")
        assert response.status_code == 200
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['name'] == 'Wyndham Capital Mortgage'
        assert len(response_json['reviews']) > 1

    def test_fetch_by_vendor(self):
        response = self.controller.get_lender_reviews("1127425","wyndham-capital-mortgage", "mortgage")
        assert response.status_code == 200
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['name'] == 'Wyndham Capital Mortgage'
        assert len(response_json['reviews']) > 1

    def test_fetch_by_vendor_with_bad_name(self):
        with pytest.raises(ExceptionResponse) as error:
            response = self.controller.get_lender_reviews("1127425","wyndham-capdfdital-mortgage", "")
        assert(error.value.to_dict()['message']) == "Invalid URI/parameters passed"



    def test_fetch_by_vendor_without_LenderId(self):
        response = self.controller.get_lender_reviews("0","wyndham-capital-mortgage", "mortgage")
        assert response.status_code == 200
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['name'] == 'Wyndham Capital Mortgage'
        assert len(response_json['reviews']) > 1
