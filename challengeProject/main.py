from flask import Flask, jsonify
from requests import request
from flask import request as req
from bs4 import BeautifulSoup
from challengeProject.models import *
import re


def create_app():
    application = Flask(__name__)
    application.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    return application

app = create_app()

@app.route("/")
def hello():
    return "Hi, try hitting the /lenders endPoint with a Name and VendorType, or if you know the full uri, hit /reviews with the uri as Link"

@app.route('/lenders/<lender_id>',methods=['GET'])
def get_lender_reviews(lender_id):
    name=req.args.get("Name")
    vendor_type = req.args.get("VendorType")

    if name is None:
        raise ExceptionResponse("Name is a required parameter", 400)
    if vendor_type is None:
        raise ExceptionResponse("Type is a required parameter ", 400)
    name = re.sub(r'[_+]|%20','-',str(name).lower())
    vendor_type = re.sub(r'[_+]|%20','-',str(vendor_type).lower())

    if len(name) == 0:
        raise ExceptionResponse("Name cannot be blank", 400)
    if len(vendor_type) == 0:
        raise ExceptionResponse("Type cannot be blank", 400)

    base_uri = "https://www.lendingtree.com/reviews/{}/{}/{}"
    full_uri = None
    if lender_id is None:
        full_uri = base_uri.format(vendor_type,name,'')
    else:
        full_uri = base_uri.format(vendor_type,name,lender_id)
    lender = Lender(name.title())
    return get_reviews_by_uri(full_uri, lender)

@app.route('/reviews', methods=['GET'])
def get_reviews_by_uri(uri=None, lender=None):
    if uri is None:
        uri=req.args.get("Link")
    if uri is None:
        raise ExceptionResponse("Link is a required parameter", 400)
    uri = str(uri)
    if len(uri) == 0 :
        raise ExceptionResponse("Link cannot be blank")
    response = request("GET", uri)
    soup = BeautifulSoup(response.text, 'html.parser')
    if lender is None:
        lender = Lender(soup.find("div",{"class": "lenderInfo"}).find("h1").text)
    details = soup.find_all("div", {"class": "reviewDetail"})
    ratings = soup.find_all("div", {"class": "recommended"})
    points = soup.find_all("div", {"class": "reviewPoints"})
    try:
        for i in range(len(details)):
            review = Review()
            if ratings[i] is not None:
                rating_soup = BeautifulSoup(str(ratings[i]), 'html.parser')
                review.star_rating = rating_soup.find("div",{"class":"numRec"}).text
            detail_soup = BeautifulSoup(str(details[i]), 'html.parser')
            review.title = detail_soup.find("p",{"class": "reviewTitle"}).text
            review.text = detail_soup.find("p", {"class": "reviewText"}).text
            review.author = detail_soup.find("p", {"class": "consumerName"}).text.replace("                                                                        ", " ")
            review.date = detail_soup.find("p", {"class": "consumerReviewDate"}).text
            points_soup = BeautifulSoup(str(points[i]), 'html.parser')
            if points[i] is not None:
                loan_type = points_soup.find("div", {"class": "loanType"})
                if loan_type is not None:
                    review.loan_type = loan_type.text
            lender.add_review(review)
    except:
        raise ExceptionResponse("An Error Occurred",500)
    return jsonify(lender.serialize())
    # return "success"
if __name__ == "__main__":
    app.run()

@app.errorhandler(ExceptionResponse)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
