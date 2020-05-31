from challengeProject import main
import json
import flask
import pytest
import requests


app = main.create_app()
app.config['TESTING'] = True
def test_context():
    with app.test_request_context('/reviews?Link=https://www.lendingtree.com/reviews/mortgage/wyndham-capital-mortgage/1127425'):
        assert flask.request.path == '/reviews'
        assert flask.request.args['Link']=='https://www.lendingtree.com/reviews/mortgage/wyndham-capital-mortgage/1127425'

def test_missing_params():
    with app.test_client() as c:
        response = c.get('/reviews')
        assert response.status_code == 400
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['message'] == "Link is a required parameter"
        response = c.get('/reviews?Link=')
        assert response.status_code == 400
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['message'] == "Link cannot be blank"

        response = c.get('/lenders/0')
        assert response.status_code == 400
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['message'] == "Name is a required parameter"
        response = c.get('/lenders/0?Name=test')
        assert response.status_code == 400
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['message'] == "VendorType is a required parameter"
        response = c.get('/lenders/0?Name=&VendorType=test')
        assert response.status_code == 400
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['message'] == "Name cannot be blank"

def test_bad_format_requests():
    with app.test_client() as c:
        response = c.get('/revieeeews')
        assert response.status_code == 404

        response = c.get('/reviews?Link=0')
        assert response.status_code == 400
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['message'] == "Invalid URI/parameters passed"

def test_vendor_not_found():
    with app.test_client() as c:
        response = c.get('/lenders/0?Name=test&VendorType=test')
        assert response.status_code == 500
        response_json = json.loads(response.data.decode('utf-8'))
        assert response_json['message'] == "Couldnt find full reviews uri for lender named: test of type: test"