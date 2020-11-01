import requests
r = requests.post('https://ka-sales-prediction-app.herokuapp.com/predict', json = {
"Store":1111,
"DayOfWeek":4,
"Date":"2014-07-10",
"Sales":4507,
"Customers":410,
"Open":0,
"Promo":0,
"StateHoliday":"0",
"SchoolHoliday":1
})

print(r.text)