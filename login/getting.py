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

@app.route("/template",methods=["POST","GET"])
def contact_information():
    print("and")
    if request.method == 'GET':
        value=session.get('email')
        # value=(value1)
        #value=str(value1)
        print(value)
        cnx = create_db_connection()
        cursor = cnx.cursor()
        #query = "SELECT * FROM contact_information"
        
        cursor.execute("SELECT * FROM personal_information WHERE user_id=%s",(value,))
        var_1 = cursor.fetchone()

        firstname=var_1[1],lastname=var_1[2],dob=str(var_1[3])
        personal=jsonify({'firstname':firstname,'lastname':lastname,'dob':dob})
        cnx.close()
        cnx = create_db_connection()
        cursor = cnx.cursor()
        #query = "SELECT * FROM contact_information"
        
        cursor.execute("SELECT * FROM contact_information WHERE user_id=%s",(value,))
        var_2 = cursor.fetchone()
        alternate_email=var_2[1],phone_number=var_2[2],alternate_number=var_2[3],address=var_2[4],linkedin_url=var_2[5]
        contact=jsonify({'alternate_email':alternate_email,'phone_number':phone_number,'alternate_number':alternate_number,'address':address,'linkedin_url':linkedin_url})
        cnx.close()
        cnx = create_db_connection()
        cursor = cnx.cursor()
        #query = "SELECT * FROM work_experience"
        cursor.execute("SELECT * FROM work_experience WHERE user_id=%s",(value,))
        var_3 = cursor.fetchall()
        experience=[]
        for work in var_3:
            company_name=work[1]
            position=work[2]
            start_date=work[3]
            start_date=start_date.strftime('%d-%m-%y')
            current_job=work[4]
            current_job=str(current_job)
            end_date=work[5]
            end_date=end_date.strftime('%d-%m-%y')
            experience.append(jsonify({company_name:'company_name'
                       ,position:'position'
                       ,start_date:'start_date'
                       ,current_job:'current_job'
                       ,end_date:'end_date'}))
        cnx.close()
        #print(var_2)
        #query = "SELECT * FROM skills"
        cnx = create_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM skills Where user_id=%s",(value,))
        var_4 = cursor.fetchall()
        skill=[]
        for skills in var_4:
            skill_name=skills[1]
            skill_level=skills[2]
            skill.append(jsonify({skill_name:'skill_name'
                       ,skill_level:'skill_level'
                       }))
        cnx.close()
        #query = "SELECT * FROM education"
        cnx = create_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM education WHERE user_id=%s",(value,))

        var_4 = cursor.fetchall()
        education=[]
        for education1 in var_4:
            school_name=education1[1]
            education_qualification=education1[2]
            cgpa=education1[3]
            cgpa=str(cgpa)
            passing_year=education1[4]
            passing_year=str(passing_year)
            education.append(jsonify({school_name:'school_name'
                       ,education_qualification:'education_qualification'
                       ,cgpa:'cgpa'
                       ,passing_year:'passing_year'}))
        cnx.close()
        #query = "SELECT * FROM project"
        cnx = create_db_connection()
        cursor = cnx.cursor()
        
        cursor.execute("SELECT * FROM project WHERE user_id=%s",(value,))
        var_5 = cursor.fetchall()
        project1=[]
        for project in var_5:
            project_name=project[1]
            project_description=project[2]
            implementation_year=project[3]
            implementation_year=str(implementation_year)
            project1.append(jsonify({project_name:'project_name'
                       ,project_description:'project_description'
                       ,implementation_year:'implementation_year'}))
            
        cnx.close()
        #query = "SELECT * FROM certification"
        cnx = create_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM certification WHERE user_id=%s",(value,))
        var_6 = cursor.fetchall()
        certificate1=[]
        for certificate in var_6:
            certification_name=certificate[1]
            issued_by=certificate[2]
            certification_id=certificate[3]
            certificate1.append(jsonify({certification_name:'certification_name'
                       ,issued_by:'issued_by'
                       ,certification_id:'certification_id'}))
        cnx.close()
        #query = "SELECT * FROM hobbies"
        cnx = create_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM hobbies WHERE user_id=%s",(value,))
        var_7 = cursor.fetchall()
        hobby1=[]
        for hobby in var_7:
            hobbi=hobby[1]
            hobby1.append(jsonify({hobbi:'hobbi'}))
        cnx.close()
        #return jsonify({'alternate_email': var_1[1], 'phone_number': var_1[2],'alternate_number': var_1[3],'address':var_1[4],'linkedin_url': var_1[5]})
        return jsonify({'personal':personal,'contact':contact,'work_experience':experience,'skill':skill,'education':education,'project':project1,'certificate':certificate1,'hobby': hobby1})


# def work_experience():
#     print("and")
#     if request.method == 'GET':
#         cnx = create_db_connection()
#         cursor = cnx.cursor()
#         query = "SELECT * FROM work_experience"
#         cursor.execute(query)
#         var_1 = cursor.fetchone()
#         query = "SELECT * FROM skills"
#         cursor.execute(query)
#         var_1 = cursor.fetchone()
#         query = "SELECT * FROM project"
#         cursor.execute(query)
#         var_1 = cursor.fetchone()
#         return jsonify({'company_name': var_1[1], 'position': var_1[2],'start date': var_1[3],'current job': var_1[4],'end date':var_1[5]})

# def skills():
#     print("and")
#     if request.method == 'GET':
#         cnx = create_db_connection()
#         cursor = cnx.cursor()
#         query = "SELECT * FROM skills"
#         cursor.execute(query)
#         var_1 = cursor.fetchone()
#         return jsonify({'skill_name': var_1[1], 'level':var_1[2]})
    
# def education():
#     print("and")
#     if request.method == 'GET':
#         cnx = create_db_connection()
#         cursor = cnx.cursor()
#         query = "SELECT * FROM education"
#         cursor.execute(query)
#         var_1 = cursor.fetchone()
#         return jsonify({'school_name': var_1[1], 'qualification':var_1[2], 'cgpa': var_1[3],'passing_year':var_1[4]})

# def Project():
#     print("and")
#     if request.method == 'GET':
#         cnx = create_db_connection()
#         cursor = cnx.cursor()
#         query = "SELECT * FROM project"
#         cursor.execute(query)
#         var_1 = cursor.fetchone()
#         return jsonify({'project_name': var_1[1], 'project_description':var_1[2], 'implementation_year': var_1[3]})

# def Certification():
#     print("and")
#     if request.method == 'GET':
#         cnx = create_db_connection()
#         cursor = cnx.cursor()
#         query = "SELECT * FROM certification"
#         cursor.execute(query)
#         var_1 = cursor.fetchone()
#         return jsonify({'certification_name': var_1[1], 'issued_by':var_1[2], 'certification_id': var_1[3]})
    
# def Hobbies():
#     print("and")
#     if request.method == 'GET':
#         cnx = create_db_connection()
#         cursor = cnx.cursor()
#         query = "SELECT * FROM hobbies"
#         cursor.execute(query)
#         var_1 = cursor.fetchone()
#         return jsonify({'hobby': var_1[1]})




if __name__ == '__main__':
    app.run(debug=True, port=5000)

        