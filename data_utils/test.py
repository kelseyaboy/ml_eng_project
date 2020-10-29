from Model import Model

json = {"Store":1111,
"DayOfWeek":4,
"Date":"2014-07-10",
"Sales":4507,
"Customers":410,
"Open":1,
"Promo":0,
"StateHoliday":"0",
"SchoolHoliday":1}

model = Model()
model.read_data(json)
print(model.snippet)
model.prepare()