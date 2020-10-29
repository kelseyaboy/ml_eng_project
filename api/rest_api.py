from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from mynt_project.ml_eng_project import data_utils
from data_utils import Model

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        expected_fields = ['Store', 'DayOfWeek', 'Date', 'Sales', 'Customers', 
                           'Open', 'Promo', 'StateHoliday', 'SchoolHoliday']

        for field in expected_fields:
            parser.add_argument(field)
        
        args = parser.parse_args()

        model = Model()
        model.read_data(args)
        model.prepare()
        pred_sales = model.predict()

        return {'sales': pred_value}

api.add_resource(HelloWorld, '/predict')


if __name__ == '__main__':
    app.run(debug=True)