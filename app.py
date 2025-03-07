#import libraries:
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
import sqlite3
import random
import string

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)

DATABASE = "referral_system.db"

# connect to DB
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# generating unique referral codes
def gen_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# User Registration API
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email, name, mobile, city, password = data.get('email'), data.get('name'), data.get('mobile'), data.get('city'), data.get('password')
    referral_code = data.get('referral_code')

    if not all([email, name, mobile, city, password]):
        return jsonify({"error": "All fields except referral_code are required"}), 400

    conn = connect_db()
    cur = conn.cursor()

    # Check if email already exists
    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_referral_code = gen_ref_code()

    # Insert new user
    cur.execute("INSERT INTO users (email, name, mobile, city, referral_code, password_hash) VALUES (?, ?, ?, ?, ?, ?)", 
                (email, name, mobile, city, user_referral_code, hashed_password))
    conn.commit()
    user_id = cur.lastrowid

    # If referral code is provided, validate and insert referral record
    if referral_code:
        cur.execute("SELECT id FROM users WHERE referral_code = ?", (referral_code,))
        referrer = cur.fetchone()
        if referrer:
            referrer_id = referrer[0]
            cur.execute("INSERT INTO referrals (referrer_id, referee_id) VALUES (?, ?)", (referrer_id, user_id))
            conn.commit()
        else:
            return jsonify({"error": "Invalid referral code"}), 400

    cur.close()
    conn.close()
    return jsonify({"message": "User registered successfully", "referral_code": user_referral_code}), 201

# User Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email'), data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.check_password_hash(user["password_hash"], password):
        access_token = create_access_token(identity=user["id"])
        return jsonify({"user_id": user["id"], "email": email, "access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Get Referrals API
@app.route('/referrals/<int:user_id>', methods=['GET'])
def get_referrals(user_id):
    print(user_id)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.name, u.email, u.created_at 
        FROM referrals r 
        JOIN users u ON r.referee_id = u.id 
        WHERE r.referrer_id = ?
    """, (user_id,))
    referrals = [{"name": row["name"], "email": row["email"], "registration_date": row["created_at"]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(referrals), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

