import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://realtimeattendence-b281a-default-rtdb.firebaseio.com/"
})

ref=db.reference('Students')

data={
    "2101053CS":{
        "name":"Shivam Kumar",
        "major":"CSE",
        "starting_year":2021,
        "total_attendence":10,
        "standing":"G",
        "Year":4,
        "last_attendence_time":"2024-11-20 10:20:00"
    },
    "2101084CS":{
        "name":"Omkar Omar",
        "major":"CSE",
        "starting_year":2021,
        "total_attendence":10,
        "standing":"G",
        "Year":4,
        "last_attendence_time":"2024-11-20 10:20:00"
    },
    "2101199EC":{
        "name":"Rittik Raj",
        "major":"ECE",
        "starting_year":2021,
        "total_attendence":4,
        "standing":"B",
        "Year":4,
        "last_attendence_time":"2024-11-20 10:20:00"
    }
}

for key,value in data.items():
    ref.child(key).set(value)