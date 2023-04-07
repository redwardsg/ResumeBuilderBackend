from flask import Flask, request, jsonify,session
import datetime
#from database import create_db_connection,test_db_connection
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

def create_db_connection():
    print("Connected")
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

@app.route('/signup', methods = ['POST'])
def register():
    print("Register")
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        dob = request.form['dob']
        email = request.form['email']
        mobile_number = request.form['mobile-number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match'})
        cnx = create_db_connection()
        cursor = cnx.cursor()
        last_updated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #query = "INSERT INTO user_table(email,password,is_active,last_updated,HasContent) VALUES (%s, %s, %s, %s, %s)"
        query_1="INSERT INTO user_table(user_id,email,password,isactive,lastupdated,has_resume_content) VALUES (%s,%s,%s,%d,%Y-%m-%d %H:%M:%S,%d)"
        #values = (email,password,'1',last_updated,0)
        values_1=(email,email,password,'1',last_updated,'0')

if __name__ == '__main__':
    app.run(debug=True, port=5000) 

