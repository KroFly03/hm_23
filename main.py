from flask import Flask, request
from flask_restx import Namespace, Resource, Api

import utils
from exceptions import BaseError

app = Flask(__name__)

query = Namespace('perform_query')
api = Api(app)
api.add_namespace(query)


@query.route('/')
class QueryView(Resource):
    def post(self):
        try:
            data = request.args
            return utils.execute_query(data)
        except BaseError as ex:
            return str(ex.message), 400


if __name__ == '__main__':
    app.run(debug=True)
