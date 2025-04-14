import requests
import datetime
import pytz

url = "api to backend for exercise"
headers = {
        "x-app-id": API_ID,
        "x-app-key": API_KEY
    }
def findx(user_input, gender, weight, height, age, headers=headers):
    tz_ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(tz_ist)
    date, time = str(now_ist.strftime("%Y-%m-%d %H:%M:%S")).split(" ")
    query = {
     "query": user_input,
     "gender": gender,
     "weight_kg": weight,
     "height_cm": height,
     "age": age
    }
    response = requests.post(url=url, json=query, headers=headers)
    print(response.raise_for_status())
    print(response.json())
    data = response.json()['exercises']
    print(data)
    new=[]
    for each_exercise in data:
        exercise = {
            'exercise': each_exercise['user_input'],
            'duration': each_exercise['duration_min'],
            'calories': each_exercise['nf_calories'],
            'date': date,
            'time': time,
            'description': user_input,
        }
        new.append(exercise)
    # print(new)
    return  new




url_food  ='api to front end'
headers_food = {
    "x-app-id": api_food,
    "x-app-key": api_key_food
}
def find_food(user_input):
    tz_ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(tz_ist)
    date, time = str(now_ist.strftime("%Y-%m-%d %H:%M:%S")).split(" ")
    query = {
        "text": user_input,
    }
    response = requests.post(url=url_food, json=query, headers=headers_food)
    print(response.text)

    data = response.json().get('found', {})
    missing = response.json().get('missing', [])
    print(data, missing, 'what and ahy')
    food = []
    for food_name in data.keys():
        each_food = data[food_name]
        # print(each_food)
        # print(type(each_food))
        foods ={
            'food': food_name,
            'date': date,
            'time': time,
            'serving_unit': each_food['value'],
            'description': user_input,
            'calories': each_food['calories'],
            'protein': each_food['protein'],
            'carbohydrates': each_food['carbohydrates'],
            'sugar': each_food['sugar'],
            'sodium': each_food['sodium'],
            'quantity': each_food['quantity'],
            'fiber': each_food['fiber'],
        }
        # print(each_food)
        food.append(foods)
    return food,missing




