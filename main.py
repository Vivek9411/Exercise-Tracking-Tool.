import requests
import datetime
import os



# log on to nutritionix.com set apiid to variable API_id and api key to APIKEY variable
API_ID = "******" # nutritionix.com
API_KEY = "****************"



url = "https://trackapi.nutritionix.com/v2/natural/exercise"  # api url of nutritionix.com

#link to sheety to google sheets and save the  api addsress of google sheet gebetared by sheety
sheet_url = "https://api.sheety.co/2d693859d068840c30e5f876368734a7/workouts/sheet1"

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY
}

query = {
 "query": input("Tell me which exercise you do? "),
 "gender": "male",
 "weight_kg": 50,
 "height_cm": 157.64,
 "age": 22
}

response = requests.post(url=url, json=query, headers=headers)
print(response.raise_for_status())
print(response.json())
data = response.json()['exercises']
exercise = []  # all things
duration = 0  # in min
calories = 0  # in kcal


date = datetime.date.today().strftime("%d/%m/%Y")
print(date)
time_ = datetime.datetime.now().time().strftime("%H:%M:%S")
print(time_)


headers = {
    "Authorization": "******" # authorisation token od sheeety
}
for items in data:
    exercise = items['user_input']
    duration = items['duration_min']
    calories = items['nf_calories']
    dict_ = {
        "sheet1": {
            "date": str(date),
            "time": str(time_),
            "exercise": str(exercise),
            "duration": str(duration),
            "calories": str(calories)
        }
    }
    response1 = requests.post(url=sheet_url, json=dict_, headers=headers)
    print(response1.json())
    print(response1.raise_for_status())

# response = requests.get(url=sheet_url)
# print(response.json())
