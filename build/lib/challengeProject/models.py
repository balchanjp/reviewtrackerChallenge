
class Review:
    def __init__(self, title=None, text=None, author=None, date=None, star_rating=None, loan_type=None):
        self.title = title
        self.text = text
        self.author = author
        self.star_rating = star_rating
        self.date = date
        self.loan_type = loan_type
    #     self.extra_data = {}
    # def add_data(self, name, value):
    #     self.extra_data.__setitem__(name, value)
    def serialize(self):
        return {
            'title' : self.title,
            'text' : self.text,
            'author' : self.author,
            'star_rating' : self.star_rating,
            'date' : self.date,
            'loan_type' : self.loan_type
        }

class Lender:

    def __init__(self, name):
        self.name = name
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def serialize(self):
        return {
            'name' : self.name,
            'reviews' : [review.serialize() for review in self.reviews]
        }


class ExceptionResponse(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        value = dict(self.payload or ())
        value['message'] = self.message
        return value
