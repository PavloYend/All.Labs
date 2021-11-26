import requests

# r = requests.put("http://localhost:5000/user/2", json={'username':'username1'})
# print(r.text)

#r = requests.post("http://localhost:5000/user", json={'username':'username2', "firstName":"Petro", "lastName":"d","email":"pet@gmail.com","phone":"097684532","password":"4568",})
# print(r.text)

r = requests.delete("http://localhost:5000/user/11", json={'jwt':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjExfQ.7j2TwRdLzqS1eIpTSgyR_-diaNQ7Yp0M9FLLMSyUYOY'})
print(r.text)
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjd9.pacsMPR3i6bQ_ug-KDH6AFbvhCirvpk5JrTdmEERyuU usID 7

#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjh9.sy-CXAl-CCQg0It6J1zuEPYeyh8rPRGv-Fa1u1G4pB4 usID 8

#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwfQ.mMsexaGnBLC8Se7BUFdzrLUr4H98_3f0_8AqeFVb7ek 10

#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjExfQ.7j2TwRdLzqS1eIpTSgyR_-diaNQ7Yp0M9FLLMSyUYOY 11