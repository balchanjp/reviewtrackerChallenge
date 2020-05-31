from requests import request
from flask import jsonify
from bs4 import BeautifulSoup
from challengeProject.models import *
import re


class MainController:
    def __init__(self, app):
        self.app = app


    def hello(self):
        return "Hi, try hitting the /lenders endPoint with an id or a Name and VendorType with an id of 0, or if you know the full uri, hit /reviews with the uri as Link"


    def get_lender_reviews(self,lender_id, name, vendor_type):
        base_uri = "https://www.lendingtree.com/reviews/{}/{}/{}"
        full_uri = None

        if lender_id is not None and lender_id != '0':
            full_uri = base_uri.format(vendor_type, name, lender_id)
        else:
            short_uri = "https://www.lendingtree.com/reviews/{}/{}".format(vendor_type,name).replace(' ','-')
            response = request("GET", short_uri)

            soup = BeautifulSoup(response.text, 'html.parser')
            endpoint = soup.find("a", {"class": "all-customer-review-link"})
            if endpoint is None:
                raise ExceptionResponse("Couldnt find full reviews uri for lender named: {} of type: {}".format(name, vendor_type), 500)
            full_uri = "https://www.lendingtree.com{}".format(endpoint['href'])

        lender = Lender(re.sub(r'[-]',' ',name.title()))
        return self.get_reviews_by_uri(full_uri, lender)


    def get_reviews_by_uri(self,uri=None, lender=None):
        response = None
        try:
            response = request("GET", uri)
        except:
            raise ExceptionResponse("Invalid URI/parameters passed", 400)
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


