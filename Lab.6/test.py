import requests

# r = requests.put("http://localhost:5000/user/2", json={'username':'username1'})
# print(r.text)

#r = requests.post("http://localhost:5000/user", json={'username':'username2', "firstName":"Petro", "lastName":"d","email":"pet@gmail.com","phone":"097684532","password":"4568",})
# print(r.text)

r = requests.post("http://localhost:5000/user", json={'username':'username5', "firstName":"Mykol", "lastName":"k","email":"myt@gmail.com","phone":"46687","password":"12345",})
print(r.text)