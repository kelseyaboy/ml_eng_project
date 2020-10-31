from flask import Flask
from flask_restful import Resource, Api, reqparse
from api import Model

app = Flask(__name__)
api = Api(app)


class SalesPredictor(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        expected_fields = ['Store', 'DayOfWeek', 'Date', 'Sales', 'Customers', 
                           'Open', 'Promo', 'StateHoliday', 'SchoolHoliday']

        for field in expected_fields:
            parser.add_argument(field)
        
        args = parser.parse_args()

        model = Model.Model()
        model.read_data(args)
        model.prepare()
        pred_sales = model.predict_sales().tolist()

        if len(pred_sales)==0:
            pred_sales = float(0)
        else:
            pred_sales = float(pred_sales[0])
        return {'sales': pred_sales}

api.add_resource(SalesPredictor, '/predict')