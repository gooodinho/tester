# Test task
A web application to retrieve user data from csv and xml files.

The csv files should store the username, password and date_joined users. The xml files should contain first_name, last_name and a link to the avatar. 
1) The format of the files must match the test_*.csv/xml templates in the media directory.
2) The username of the user must be created according to the template - "First letter first_name.last_name".
3) If some data about user will be absent in files, such users will not be saved. Also, users whose data has round or square brackets. 
4) Only users who are super-user can add users from files. 

## To start the application locally

1) You must have Python installed.
2) Install all the libraries from the requirements.txt files.
`pip install -r requirements.txt`
3) Rename file `.env.example` to `.env` and paste your SECRET_KEY there.

**If you want to run application with sqlite3 as db:**

1) `python manage.py makemigrations`
2) `python manage.py migrate`

*If you want to run application with PostgreSQL as db:*

*1) Install PostgreSQL locally.*

*2) Open pgadmin or pg bash and create new db.*

*3) Uncomment code `Connecting to PostgreSQL` in `settings.py` and fill db data in `.env` file.*


**Then create super user `python manage.py createsuperuser`**

**Run server locally `python manage.py runserver`. Go to the ip where your server is running (*http://127.0.0.1:8000/*).**

**Login as the superuser you created before.**

Use test files from /media directory. And try to add new users. If new users have been added, all users will be displayed on the main page. 

Their credentials can be used to log in to the application, but the data collection function is not available for them. 