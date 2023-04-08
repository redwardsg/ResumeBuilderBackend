from flask import Flask, request,jsonify,render_template,redirect, url_for,session
import mysql.connector
from mysql.connector import errorcode
import datetime 

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
    'password': '9390',
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

@app.route('/signup', methods=['POST'])
def signup():
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
        query = "SELECT * FROM users WHERE email=%s and password=%s"
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




@app.route('/save_data',methods = ['GET','POST'])

def save_section():
    if request.method == 'POST':
        value=session.get('email')
        print(f'it is {value}')
        data=request.get_json()
        personalInfoData=data['personaInfoData']
        firstname = personalInfoData['firstName']
        lastname = personalInfoData['lastName']
        dob = personalInfoData['dateofBirth']
        dob_1=datetime.strptime(dob, '%d-%m-%Y').strftime('%d-%m-%y')
        #session["email"]=email
        cnx = create_db_connection()
        cursor = cnx.cursor()
        query_personal = "INSERT INTO personal_information(user_id,firstname, lastname, dob) VALUES (%s,%s,%s, %s)"
        values_personal = (value,firstname, lastname, dob_1)
        cursor.execute(query_personal, values_personal)
        cnx.commit()
        #print(firstname)
        cnx.close()
       
    




        contactInfoData=data['contactInfoData']
        alternate_email = contactInfoData['alternate_email']
        phone_number = contactInfoData['phoneNumber']
        alternate_number = contactInfoData['alternateNumber']
        address=contactInfoData['address']
        linkedin_url = contactInfoData['linkdin']
        cnx = create_db_connection()
        cursor = cnx.cursor()
        query_contact = "INSERT INTO contact_information(user_id,alternate_email, phone_number, alternate_number,address, linkedin_url) VALUES (%s, %s, %s, %s,%s,%s)"
        values_contact = (value,alternate_email, phone_number, alternate_number,address, linkedin_url)
        cursor.execute(query_contact, values_contact)
        cnx.commit()
        cnx.close()
    




        for workExperience in data['workExperienceInfo']:
            company_name = workExperience['companyName']
            position = workExperience['position']
            start_date = workExperience['date']
            start_date1=datetime.strptime(start_date, '%d-%m-%Y').strftime('%d-%m-%y')
            current_job = workExperience['currentJob']
            end_date = workExperience['endDate']
            end_date1=datetime.strptime(end_date, '%d-%m-%Y').strftime('%d-%m-%y')
            cnx = create_db_connection()
            cursor = cnx.cursor()
            query_work = "INSERT INTO work_experience(user_id,company_name,position,start_date,current_job,end_date) VALUES (%s,%s,%s,%s,%s,%s)"
            values_work = (value,company_name,position,start_date1,current_job,end_date1)
            cursor.execute(query_work, values_work)
            cnx.commit()
            cnx.close()


 
 
        for skill in data['skillInfoData']:
            skill_name = skill['skillName']
            print(skill_name)
            level = skill['skillLevel']
            cnx = create_db_connection()
            cursor = cnx.cursor()
            query_skill = "INSERT INTO skills(user_id,skill_name,skill_level) VALUES (%s,%s,%s)"
            values_skill = (value,skill_name,level)
            cursor.execute(query_skill, values_skill)
            cnx.commit()
            cnx.close()

 
 
        for education in data['educationInfoData']:

            school_name = education['schoolname']
            qualification = education['qualification']
            cgpa = education['cgpa']
            passing_year = education['passing_year']
            cnx = create_db_connection()
            cursor = cnx.cursor()
            query_education = "INSERT INTO education(user_id,school_name,education_qualification,cgpa,passing_year) VALUES (%s,%s,%s,%s,%s)"
            values_education = (value,school_name,qualification,cgpa,passing_year)
            cursor.execute(query_education, values_education)
            cnx.commit()
            cnx.close()



 
 
        for project in data['projectInfoData']:
            project_name= project['projectname']
            project_description = project['projectDescription']
            implementation_year = project['ImplementationYear']
            cnx = create_db_connection()
            cursor = cnx.cursor()
            query_project = "INSERT INTO project(user_id,project_name,project_description,implementation_year) VALUES (%s,%s,%s,%s)"
            values_project = (value,project_name,project_description,implementation_year)
            cursor.execute(query_project, values_project)
            cnx.commit()
            cnx.close()




       
        for certificate in data['certificateInfoData']:
            
            certification_name = certificate['certification']
            issued_by = certificate['issued_by']
            certification_id = certificate['certification_id']
            cnx = create_db_connection()
            cursor = cnx.cursor()
            query_certification = "INSERT INTO certification(user_id,certification_name,issued_by,certification_id) VALUES (%s,%s,%s,%s)"
            values_certification = (value,certification_name,issued_by,certification_id)
            cursor.execute(query_certification, values_certification)
            cnx.commit()
            cnx.close()
        



        for hobby in data['hobbiesInfoData']:

            hobbi= hobby['hobbies']
            cnx = create_db_connection()
            cursor = cnx.cursor()
            query_hobby = "INSERT INTO hobbies(user_id,hobby) VALUES (%s,%s)"
            values_hobby = (value,hobbi)
            cursor.execute(query_hobby, values_hobby)
            cnx.commit()
            cnx.close()
            return jsonify({'status': 201, 'success': 'True', 'message': 'Details inserted successfully'})





if __name__ == '__main__':
    app.run(debug=True, port=5000)