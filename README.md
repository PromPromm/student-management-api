# Student-management-api

<a name="readme-top"></a>

  ### Table of Contents
  <ul>
    <li><a href="#live-app-version">Live App Version</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#technologies-used">Technologies used</a></li>
    <li><a href="#libraries-used">Libraries used</a></li>    
    <li><a href="#to-run-on-your-local-machine">To run on your local machine</a></li>
    <li><a href="#contact">Contact</a></li>
    <li>
      <a href="#endpoints">Endpoints</a>
      <ol>
        <li><a href="#auth-endpoints">Auth Endpoints</a></li>
        <li><a href="#course-endpoints">Course Endpoints</a></li>
        <li><a href="#student-endpoints">Student Endpoints</a></li>
        <li><a href="#admin-endpoints">Admin Endpoints</a></li>
      </ol>
    </li>
  </ul>
 
### Live app version
Visit [website](https://student-management-app-api.herokuapp.com/swagger-ui)
#### Super administrator auth details on live app
email - admin@admin.com
password - admin
 <p align="right"><a href="#readme-top">back to top</a></p>


### About
This is a student management REST api that enables the school authorities(admin) to manage students and allow students to login and check cgpa.
Students have limited access to the app in terms of the number of routes they can access, admin have unlimited access to student and course routes.
The super admin has unlimited access to all routes in the app
<p align="right"><a href="#readme-top">back to top</a></p>


### Technologies Used
- Python
- Flask
- SQLite
 <p align="right"><a href="#readme-top">back to top</a></p>


### Libraries Used
- [Flask smorest](https://flask-smorest.readthedocs.io/) - framework for creating REST api
- [Flask migrate](https://flask-migrate.readthedocs.io/) - framework for tracking database modifications
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - object relational mapper
- [Flask JWT extended](https://flask-jwt-extended.readthedocs.io/en/stable/) - authentication and authorization
<p align="right"><a href="#readme-top">back to top</a></p>


### To run on your local machine
Clone the repository
```console
git clone https://github.com/PromPromm/student-management-api
```
Navigate into the project folder
```console
cd student-mgt-app
```
Install the required dependencies
```console
pip install -r requirements.txt
```
Intanstiate Database
```console
flask db init
```
```console
flask db migrate
```
```console
flask db upgrade
```
Navigate to `runserver.py` and change line 4 to:
```console
app = create_app()
```
Save and close the file.

Create a `.env` file by running:
```console
touch .env
```
Copy the code below into the file.
```console
SECRET_KEY=`your secret key`
DEBUG=True
JWT_SECRET_KEY=`another secret key`
EMAIL=`email of choice for super admin`
```
Save and close the file

Run the app
```console
python runserver.py
```
 <p align="right"><a href="#readme-top">back to top</a></p>


### Contact
Promise - promiseanuoluwa@gmail.com
 <p align="right"><a href="#readme-top">back to top</a></p>


## Endpoints

### Auth Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  
| ------- | ----- | ------------ | ------|------- |
|  `/students/signup` | _POST_ | To create a student account   | Authenticated | Admin | 
|  `/admin/signup` |  _POST_ | To create an admin account   | Authenticated| Super Admin | 
|  `/student/login` |  _POST_  | To authenticate students   | ---- | Any | 
|  `/admin/login` |  _POST_  | To authenticate administrator   | ---- | Admin | 
|  `/refresh` |  _POST_  | Generate refresh token  | Authenticated | Any | 
|  `/logout` |  _DELETE_  | Logout user and revoke JWT access token | Authenticated | Any | 
 <p align="right"><a href="#readme-top">back to top</a></p>


### Course Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  VARIABLE RULE | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/course` |  _GET_  | Retrieves all courses  | Authenticated | Admin | ---- |
|  `/course` |  _POST_  | Create a new course   | Authenticated | Admin | ---- |
|  `course/<course_id>` |  _GET_  | Retrieve a course by unique identifier   | Authenticated | Admin | Course ID |
|  `course/<course_id>/enroll/<student_id>` |  _PUT_  | Enroll a student in a course | Authenticated | Admin | Course ID, Student ID |
|  `course/<course_id>/unenroll/<student_id>` |  _PUT_  | Unenroll a student in a course | Authenticated | Admin | Course ID, Student ID |
|  `courses/<student_id>` |  _GET_  | Retrieve all courses a student takes | Authenticated | Admin, Student | Course ID, Student School ID |
|  `courses/<course_id>/students` |  _GET_  | Retrieve all students taking a course | Authenticated | Admin | Course ID |
|  `courses/<course_id>/score-upload` |  _PUT_  | Upload score of student in a course | Authenticated | Admin | Course ID |
 <p align="right"><a href="#readme-top">back to top</a></p>


### Student Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/student` |  _GET_  | Retrieve all student  | Authenticated | Admin | ---- |
|  `/student/<student_id>` |  _GET_  | Retrieve user by unique identifier | Authenticated | Admin | Student ID |
|  `/student/<student_id>` |  _PUT_  | Change a student enrollment status | Authenticated | Admin | Student ID |
|  `/student/<student_id>` |  _DELETE_  | Delete a student by unique identifier | Authenticated | Admin | Student ID |
|  `/student/change_password` |  _PUT_  | Student password reset  | ---- | Student | ---- |
|  `/student/<student_id>/scores` |  _GET_  | Retrieve student scores and grades  | Authenticated | Admin, Student | Student School ID |
|  `/student/<student_id>/cgpa` |  _GET_  | Calculate and Retrieve a student gpa score   | Authenticated | Admin, Student | Student School ID |
 <p align="right"><a href="#readme-top">back to top</a></p>


### Admin Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/admin` |  _GET_  | Retrieve all administrator  | Authenticated | Admin | ---- |
|  `/admin/change_password` |  _PUT_  | Admin password reset | ---- | Admin | ---- |
|  `/admin/<admin_id>` |  _PUT_  | Delete an admin by unique identifier | Authenticated | Super Admin | Admin ID |
 <p align="right"><a href="#readme-top">back to top</a></p>

