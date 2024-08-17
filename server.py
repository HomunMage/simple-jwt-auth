from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import configparser

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'your_secret_key_here'

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Simulating a database using config values
users_db = {}
for i in range(1, 4):  # Assuming you have 3 users
    username = config.get('account', f'user{i}')
    password = config.get('account', f'password{i}')
    users_db[username] = {
        "password": password,
        "session_token": None
    }

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users_db.get(username)
    if user and user['password'] == password:
        token = generate_token(username)
        users_db[username]['session_token'] = token
        return jsonify({"success": True, "token": token})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization').split(" ")[1]
    username = verify_token(token)
    
    if username and users_db[username]['session_token'] == token:
        return jsonify({"success": True, "message": "Welcome, {}".format(username)})
    else:
        return jsonify({"success": False, "message": "Invalid or expired token"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11567)
