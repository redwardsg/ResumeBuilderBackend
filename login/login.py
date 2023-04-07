from flask import Flask, request,jsonify,render_template,redirect, url_for
import mysql.connector
from mysql.connector import errorcode

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

@app.route('/loginpage', methods=['POST'])
def login():
    # email = request.form['email']
    # password = request.form['Password']

    # add your validation and authentication code here
    print('login started')
    if request.method=='POST':
        try:
            email_1 = request.form['email']
            print(email_1)
            password_1 = request.form['password']
        except KeyError:
            # Handle the error caused by missing or invalid data in the request payload
            return jsonify({'status': 400, 'success': 'False', 'message': 'Missing or invalid data'})
        cnx = create_db_connection()
        cursor = cnx.cursor()
        query = "SELECT * FROM user_table WHERE email=%s and password=%s, (email, password)"
        cursor.execute(query)
        user = cursor.fetchone()
        cnx.close()
        if user:     
            return jsonify({'message': 'User logged in successfully'})
        else:
            return jsonify({'message': 'Invalid credentials'})

    # redirect the user to the main page if login is successful
    #return redirect(url_for('mainpage'))

@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000) 

