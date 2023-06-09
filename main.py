from flask import Flask, request, json, jsonify, redirect, session, render_template
from flask_cors import CORS
from flask_session import Session
import pdfkit

import mysql.connector
from mysql.connector import errorcode
import datetime

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.debug = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# database configuration
#9390
db_config = {
    'user': 'root',
    'password': 'R1ch@rdMcl@ne',
    'host': 'localhost',
    'port': '3306',
    'database': 'resumebuilderdb',
    'raise_on_warnings': True
}


# helper function to create database connection
@app.route('/test-db-connection')
def test_db_connection():
    print("Testing Connection")
    cnx = create_db_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT VERSION()")
    result = cursor.fetchone()
    cnx.close()
    return jsonify({'status': 'success', 'message': 'Database connected successfully', 'version': result[0]})


def create_db_connection():
    print("Connecting....")
    try:

        cnx = mysql.connector.connect(**db_config)
        print("connected")
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


# @app.route("/" , methods = ["GET"])
# def example_template():
#     return render_template("index.html")

@app.route('/download', methods=['GET'])
def download():
    print("hello")


# registration API
@app.route('/register', methods=['POST'])
def register():
    print("Register")
    if request.method == 'POST':
        data = request.get_json()
        firstname = data['firstname']
        # firstname = request.form['firstname']
        # lastname = request.form['lastname']
        # gender = request.form['gender']
        # dob = request.form['dob']
        # email = request.form['email']
        # mobile_number = request.form['mobile-number']
        # password = request.form['password']
        # confirm_password = request.form['confirm_password']
        # if password != confirm_password:
        #     return jsonify({'message': 'Passwords do not match'})
        cnx = create_db_connection()
        cursor = cnx.cursor()
        #last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO users(email,password,isactive,hascontent) VALUES (%s, %s, %s, %s)"
        values = (firstname, firstname, 1, 0)
        cursor.execute(query, values)
        cnx.commit()
        cnx.close()
        return jsonify({'status': 201, 'success': 'True', 'message': 'User registered successfully'})


global user_id

@app.route('/test-session', methods=['GET', 'POST'])
def testSession():
    if not session.get("email"):
        # if not there in the session then redirect to the login page
        return jsonify({'message': 'Invalid session'})
    else:
        return jsonify({'message': 'Valid user' + session.get('email')})

# Fetch Personal Info API
@app.route('/FetchPersonalInfo', methods=['GET'])
def FetchPersonalInfo():
    try:
        # data = request.get_json()
        # email = data['email']
        cnx = create_db_connection()
        cursor = cnx.cursor()
        query = "SELECT * FROM personalinfo WHERE email='rina.eds@gmail.com'"
        print(query)
        cursor.execute(query)
        retRecord = cursor.fetchone()
        cnx.close()
        if retRecord:
           return jsonify({'message': 'Personal Info Found', 'email' : retRecord[0], 'firstname' : retRecord[1], 'lastname' : retRecord[2], 'DOB' : retRecord[3]})
        else:
            return jsonify({'message': 'Personal Info Not Found'})
    except KeyError:
        return jsonify({'status': 400, 'success': 'False', 'message': 'Error Retrieving Data'})


# login API
@app.route('/login', methods=['POST'])
def login():
    print('login started')
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']
            print(data)
            print(email)
            print(password)
            # email_1 = request.form['email']
            # print(email_1)
            # password_1 = request.form['password']
            # print(password_1)
        except KeyError:
            # Handle the error caused by missing or invalid data in the request payload
            return jsonify({'status': 400, 'success': 'False', 'message': 'Missing or invalid data'})
        cnx = create_db_connection()
        cursor = cnx.cursor()
        query = "SELECT * FROM users WHERE email=%(email)s and password=%(password)s"
        print(query)
        cursor.execute(query,data)
        user = cursor.fetchone()
        cnx.close()
        if user:
           session["email"] = email
           return jsonify({'message': 'User logged in successfully'})
        else:
            return jsonify({'message': 'Invalid credentials'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)