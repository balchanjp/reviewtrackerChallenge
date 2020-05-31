from flask import Flask,request as req, jsonify
from challengeProject.controller import MainController
import re
from challengeProject.models import ExceptionResponse




def create_app():
    application = Flask(__name__)
    application.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    return application

app = create_app()
controller = MainController(app)
@app.route("/")
def call_hello():
    controller.hello()


@app.route('/lenders/<lender_id>',methods=['GET'])
def call_get_lender_reviews(lender_id=0):
    name = req.args.get("Name")
    vendor_type = req.args.get("VendorType")
    if name is None:
        raise ExceptionResponse("Name is a required parameter", 400)
    if vendor_type is None:
        raise ExceptionResponse("Type is a required parameter ", 400)
    name = re.sub(r'[_+]|%20', '-', str(name).lower())
    vendor_type = re.sub(r'[_+]|%20', '-', str(vendor_type).lower())
    if len(name) == 0:
        raise ExceptionResponse("Name cannot be blank", 400)
    if len(vendor_type) == 0:
        raise ExceptionResponse("Type cannot be blank", 400)
    return controller.get_lender_reviews(lender_id,name,vendor_type)

@app.route('/reviews', methods=['GET'])
def call_get_reviews_by_uri(uri):
    uri = req.args.get("Link")
    if uri is None:
        raise ExceptionResponse("Link is a required parameter", 400)
    uri = str(uri)
    if len(uri) == 0:
        raise ExceptionResponse("Link cannot be blank")
    return controller.get_reviews_by_uri(uri)
@app.errorhandler(ExceptionResponse)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run()


