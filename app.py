from flask import Flask, request, jsonify
from flask_cors import CORS
from configparser import ConfigParser

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load credentials from config.ini
config = ConfigParser()
config.read('config.ini')

FIXED_USERNAME = config.get('credentials', 'username')
FIXED_PASSWORD = config.get('credentials', 'password')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == FIXED_USERNAME and password == FIXED_PASSWORD:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11567)
