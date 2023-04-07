from flask import Flask, request,jsonify,render_template,redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime 

app = Flask(__name__)
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
    # try:
    #     cnx = mysql.connect()
    #     return cnx
    # except Exception as e:
    #     print("error while connecting to database:", e)
    

# @app.route("/" , methods = ["GET"])
# def example_template():
#     return render_template("index.html")       

# registration API
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('signupwithjs.html')

@app.route('/home')
def profile():
    return render_template('profile.html')

@app.route('/login_validation', methods=["POST"])
def login():
    
    print('login started')

    #try:
    email_1 = request.form.get('email')
    print(email_1)
    password_1 = request.form.get('password')
    #except KeyError:
                # Handle the error caused by missing or invalid data in the request payload
        #return jsonify({'status': 400, 'success': 'False', 'message': 'Missing or invalid data'})
    cnx = create_db_connection()
    cursor = cnx.cursor()
    query = 'SELECT * FROM sign_up WHERE email = % s AND password = % s', (email_1, password_1, )
    cursor.execute(query)
    user = cursor.fetchone()
    cnx.close()
    if user:     
        return jsonify({'message': 'User logged in successfully'})
    else:
        return jsonify({'message': 'Invalid credentials'})

@app.route('/signup_validation', methods = ['GET'])
def register():
    print("Register")
    print(request.form)
    if request.method=='POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        dob = request.form.get('dob')
        dob_1=datetime.strptime(dob, '%d-%m-%Y').strftime('%Y-%m-%d')
        gender = request.form.get('gender')
        email = request.form.get('email')
        mobile_number = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmpassword')
        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match'})
        cnx = create_db_connection()
        cursor = cnx.cursor()
        #last_updated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #query = "INSERT INTO user_table(email,password,is_active,last_updated,HasContent) VALUES (%s, %s, %s, %s, %s)"
        query_1="INSERT INTO sign_up(first_name,last_name,dob,gender,mobile_number,email,password) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        #values = (email,password,'1',last_updated,0)
        values_1=(firstname,lastname,dob_1,gender,mobile_number,email,password)
        cursor.execute(query_1, values_1)
        print(f'val is {firstname}')
        cnx.commit()
        cnx.close()
        return jsonify({'status': 201, 'success': 'True', 'message': 'User registered successfully'})



if __name__ == '__main__':
    app.run(debug=True, port=5000) 

