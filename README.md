# ml_eng_project

# Final notebook for model creation is : 
./notebooks/Final_Modeling_Flow.ipynb with Decision Tree algorithm

# json data
{"Store":1111,
"DayOfWeek":4,
"Date":"2014-07-10",
"Sales":4507,
"Customers":410,
"Open":1,
"Promo":0,
"StateHoliday":"0",
"SchoolHoliday":1}

# To run manually:
1. pip install -r requirements.txt 
2. run "python app.py"
3. test localhost:5000/predict with json data

# To run using deployed app on Heroku:
1. test https://ka-sales-prediction-app.herokuapp.com/predict

# To run with docker image:
1. Create a Dockerfile with:
    FROM python:3.8

    WORKDIR /app

    COPY . .

    RUN pip install -r requirements.txt

    EXPOSE 5000

    CMD ["python", "app.py"]

2. run "docker build -t name/tagname ."
3. run "docker run -p 5000:5000 name/tagname"
3. test localhost:5000/predict with json data

# Script used for CI/CD Pipeline (Jenkins):
see Jenkinsfile