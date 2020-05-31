
from challengeProject.controller import MainController
import challengeProject.main as main
import json


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


