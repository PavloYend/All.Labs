from flask import Flask, Response
from flask_bcrypt import Bcrypt
from models import *
from flask import jsonify
import json
from flask import make_response
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert
from flask_jwt import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
bcrypt = Bcrypt(app)


def encode_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def verification(id, request):
    try:
        token = request.json.get('jwt')
        temp_id = int(decode_token(token))
    except:
        return make_response(jsonify({'error': "Invalid token"}), 404)
    if temp_id != id:
        return make_response(jsonify({'error': "Verification unsuccessful"}), 404)


def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


@app.route('/user', methods=['POST'])
def create_user():
    print("create_user")
    user = User(
        username=request.json.get('username'),
        firstName=request.json.get('firstName'),
        lastName=request.json.get('lastName'),
        email=request.json.get('email'),
        phone=request.json.get('phone'),
        password=bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
    )
    tvins = (Session.query(User).filter_by(username=user.username).all())
    if tvins != []:
        return make_response(jsonify({'error': 'Username is busy'}), 404)
    try:
        Session.add(user)
        Session.commit()
    except IntegrityError:
        print('Incorrect data')
        return make_response(jsonify({'error': 'Incorrect data'}), 404)
    # tasks.append(task)
    a = to_json(user, User)
    a = a[:-1] + ", jwt: " + str(encode_token(user.id))[1:] + a[-1]
    return Response(response=a, status=200, mimetype="application/json")


@app.route("/user/<int:id>", methods=['GET'])
def get_user(id):
    try:
        a = to_json(Session.query(User).filter_by(id=id).one(), User)
        return Response(response=a, status=200, mimetype="application/json")
    except:
        return make_response(jsonify({'error': 'User not found'}), 404)


@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    if verification(id, request):
        return verification(id, request)
    print("update_user")
    u = Session.query(User).filter_by(id=id).one()
    if not u:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if request.json.get('username'):
        tvins = (Session.query(User).filter_by(username=request.json.get('username')).all())
        if tvins != []:
            return make_response(jsonify({'error': 'username is busy'}), 409)
        u.username = request.json.get('username')
    if request.json.get('firstName'):
        u.firstName = request.json.get('firstName')
    if request.json.get('lastName'):
        u.lastName = request.json.get('lastName')
    if request.json.get('email'):
        u.email = request.json.get('email')
    if request.json.get('phone'):
        u.phone = request.json.get('phone')
    if request.json.get('password'):
        u.password = request.json.get('password')
    Session.commit()

    return Response(response=to_json(u, User), status=200, mimetype="application/json")


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    if verification(id, request):
        return verification(id, request)
    try:
        user = Session.query(User).filter_by(id=id).first()
        Session.delete(user)
        Session.commit()
        return {
            "msg": "User deleted successfully",
            "id": id
        }
    except:
        return "User not found", 404


@app.route('/event', methods=['POST'])
def create_event():
    print("create_event")
    event = Event(
        name=request.json.get('name'),
        owner_id=request.json.get('owner_id'),
    )
    try:
        Session.add(event)
        Session.commit()
    except IntegrityError:
        print('Incorrect data')
        return make_response(jsonify({'error': 'Incorrect data'}), 409)
    # tasks.append(task)
    a = to_json(event, Event)
    return Response(response=a, status=200, mimetype="application/json")


@app.route('/event/<int:id>', methods=['PUT'])
def update_event(id):
    u = Session.query(Event).filter_by(id=id).first()
    if verification(u.owner_id, request):
        return verification(u.owner_id, request)
    print("Update_event")
    if not u:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if request.json.get('name'):
        u.name = request.json.get('name')
    if request.json.get('owner_id'):
        u.owner_id = request.json.get('owner_id')

    Session.commit()
    return Response(response=to_json(u, Event), status=200, mimetype="application/json")


@app.route("/event/<int:id>", methods=['GET'])
def get_event(id):
    try:
        a = to_json(Session.query(Event).filter_by(id=id).one(), Event)
        return Response(response=a, status=200, mimetype="application/json")
    except:
        return make_response(jsonify({'error': 'Event not found'}), 404)


@app.route('/event/<int:id>', methods=['DELETE'])
def delete_event(id):
    u = Session.query(Event).filter_by(id=id).first()
    if verification(u.owner_id, request):
        return verification(u.owner_id, request)
    try:
        event = Session.query(Event).filter_by(id=id).first()
        Session.delete(event)
        Session.commit()
        return {
            "msg": "Event deleted successfully",
            "id": id
        }
    except:
        return "Event not found", 404


@app.route('/event/<int:eve_id>/user/<int:use_id>', methods=['POST'])
def request_user(eve_id, use_id):
    k = Session.query(user_event).filter_by(user_id=use_id, event_id=eve_id).all()
    if k != []:
        return make_response(jsonify({'error': 'request already exist'}), 404)

    u = Session.query(User).filter_by(id=use_id).all()
    if not u:
        return make_response(jsonify({'error': 'User Not found'}), 404)
    q = Session.query(Event).filter_by(id=eve_id).all()
    if not q:
        return make_response(jsonify({'error': ' Event Not found'}), 404)

    stmt = (
        insert(user_event).values(user_id=use_id, event_id=eve_id)
    )
    try:
        connect.execute(stmt);
    except:
        return make_response(jsonify({'Error': 'Not found'}), 404)

    return make_response(jsonify({'Successful': 'operation'}), 200)


@app.route('/your_events/user/<int:id>', methods=['GET'])
def your_events(id):

    u = Session.query(User).filter_by(id=id).all()
    if not u:
        return make_response(jsonify({'Error': 'Not found'}), 404)
    a = Session.query(Event).filter_by(owner_id=id).all()
    json_data = []
    for i in a:
        json_data.append(to_json(i, Event))
    try:
        Session.commit()
    except:
        return make_response(jsonify({'Error': 'Not found'}), 404)

    return Response(response=str(json_data), status=200, mimetype="application/json")


@app.route('/event/<int:id>/users', methods=['GET'])
def get_all_requested(id):

    u = Session.query(Event).filter_by(id=id).all()
    if not u:
        return make_response(jsonify({'Error': 'Not found'}), 404)
    a = Session.query(user_event).filter_by(event_id=id).all()

    b = []
    for i in a:
        b.append(Session.query(User).filter_by(id=i.user_id).one())

    json_data = []
    for i in b:
        json_data.append(to_json(i, User))
    try:
        Session.commit()
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return Response(response=str(json_data), status=200, mimetype="application/json")


@app.route('/events/user/<int:id>', methods=['GET'])
def user_for_request(id):

    u = Session.query(User).filter_by(id=id).all()
    if not u:
        return make_response(jsonify({'error': 'Not found'}), 404)

    a = Session.query(user_event).filter_by(user_id=id).all()
    b = []
    for i in a:
        b.append(Session.query(Event).filter_by(id=i.event_id).one())

    json_data = []
    for i in b:
        json_data.append(to_json(i, Event))
    try:
        Session.commit()
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return Response(response=str(json_data), status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)