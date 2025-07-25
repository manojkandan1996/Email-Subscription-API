from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest, NotFound
import re

app = Flask(__name__)
api = Api(app)

subscriptions = []

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'

def is_valid_email(email):
    return re.match(EMAIL_REGEX, email)

class SubscribeResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'email' not in data:
            raise BadRequest("Email field is required.")

        email = data['email'].strip().lower()
        if not is_valid_email(email):
            raise BadRequest("Invalid email format.")

        if email in subscriptions:
            return {"message": "Email is already subscribed."}, 200

        subscriptions.append(email)
        return {"message": f"{email} subscribed successfully!"}, 201

    def delete(self, email):
        email = email.strip().lower()
        if email not in subscriptions:
            raise NotFound("Email not found in subscription list.")

        subscriptions.remove(email)
        return {"message": f"{email} unsubscribed successfully."}, 200

# Register routes
api.add_resource(SubscribeResource, '/subscribe', '/subscribe/<string:email>')

if __name__ == '__main__':
    app.run(debug=True)
