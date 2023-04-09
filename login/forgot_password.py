from flask import Flask, request,jsonify,render_template,redirect, url_for,session
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

from mysqlx import Session 

app = Flask(__name__)
app.secret_key = 'Bunny'
# app.config["SESSION_PERMANENT"] = True
# app.config["SESSION_TYPE"] = "filesystem"
# session(app)
# app.debug = True
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
# database configuration

db_config = {
    'user': 'root',
    'password': 'Bunny@9866',
    'host': 'localhost',
    'port': '3306',
    'database': 'resumebuilder',
    'raise_on_warnings': True
}

# mysql = MySQL(app)

# helper function to create database connection
@app.route('/test-db-connection')
def test_db_connection():
    cnx = create_db_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT VERSION()")
    result = cursor.fetchone()
    cnx.close()
    return jsonify({'status': 'success', 'message': 'Database connected successfully', 'version': result[0]})

def create_db_connection():
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

@app.route('/login', methods=['POST'])
def login():
    print('login started')
    if request.method == 'POST':
        try:
            data = request.get_json()
        except KeyError:
            # Handle the error caused by missing or invalid data in the request payload
            return jsonify({'status': 400, 'success': 'False', 'message': 'Missing or invalid data'})
        email = data['email']
        password = data['Password']
        cnx = create_db_connection()
        cursor = cnx.cursor()
        query = "SELECT * FROM sign_up WHERE email=%s and password=%s"
        values = (email, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        print(user)
        cnx.close()
        if user:
            email = data['email']
            session["email"] = email
            print(session.get('email'))
            return jsonify({'status':'true','message': 'User logged in successfully'})
        else:
            return jsonify({'message': 'Invalid credentials'})

@app.route('/register', methods=['POST'])
def register():
    print("Register")
    if request.method == 'POST':
        try:
            data = request.get_json()
            first_name = data['first_name']
            last_name = data['last_name']
            dob = data['dob']
            gender = data['gender']
            mobile_number = data['mobile_number']
            email = data['email']
            password = data['password']
        except KeyError:
            # Handle the error caused by missing or invalid data in the request payload
            return jsonify({'status': 400, 'success': 'false', 'message': 'Missing or invalid data'})
        confirm_password = data['confirm_password']
        print(mobile_number)
        if password != confirm_password:
            return jsonify({'status':'false','message': 'Passwords do not match'})
        cnx = create_db_connection()
        cursor = cnx.cursor()
        lastupdated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query_emailexists = "SELECT * FROM sign_up WHERE email=%s"
        values_emailexists = (email,)
        cursor.execute(query_emailexists, values_emailexists)
        result = cursor.fetchone()
        print(result)
        if result:
            return jsonify({'status':'false','msg':'email already exists'})
        else:
            query_signup = "INSERT INTO sign_up(first_name,last_name,dob,gender,mobile_number,email,password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
           
            values_signup = (first_name, last_name, dob, gender, mobile_number, email, password)
            query = "INSERT INTO users(user_id,email,password,isactive,lastupdated,has_resume_content) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (email, email, password, '1', lastupdated, '0')
            cursor.execute(query_signup, values_signup)
            cursor.execute(query, values)
            cnx.commit()
            cnx.close()
            return jsonify({'status': 201, 'success': 'true', 'message': 'User registered successfully'})

@app.route('/forgot_password',methods=['GET',"POST"])
def forgot():
    if request.method=="POST":
        data=request.get_json()
        user_id=data['email']
        print(user_id)
        security_question=data['Security Question']
        security_answer=data['Security Answer']
        password=data['New Password']
        cnx = create_db_connection()
        cursor = cnx.cursor()
        query="select * from sign_up where email=%s"
        cursor.execute(query,(user_id,))
        var=cursor.fetchone()
        print(var[8],var[7])
        if var[8]==security_question:
            if var[7]==security_answer:
                query="UPDATE sign_up SET password=%s WHERE email=%s"
                values=(password,user_id)
                cursor.execute(query,values)
                print('sagar')

            else:
                return jsonify({'message': 'Passwords do not match'})
        else:
            return jsonify({'message': 'Passwords do not match'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)     