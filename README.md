# REST-API-Django

A comprehensive restaurant management system built with Django and MySQL.
Features:

* Interactive digital menu
* Online reservations
* Staff and order management
* Robust security with JWT, cookies, permissions, and protected routes
* Image manipulation capabilities


Steps after cloning the repository:

1. Create and activate a virtual environment (`python -m venv env; source env/bin/activate`).
2. Install dependencies (`pip install -r requirements.txt`).
3. Create your MySQL database and configure credentials in `settings.py`.
4. Run Django migrations (`python manage.py migrate`).
5. Create a superuser (`python manage.py createsuperuser`).
6. Start the development server (`python manage.py runserver`).
7. Access the administration panel at `http://127.0.0.1:8000/admin/`.


Important:The `.env` file stores sensitive information like database credentials and secret keys. 

.env File:

DJANGO_SECRET_KEY=
DJANGO_DEBUG=
DB_ENGINE=
DB_NAME=
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_PORT=
MY_SECRET_KEY=

Instructions for Using `.env`:

1. Create a text file named `.env` in your project's root directory.
2. Copy and paste the above content into the `.env` file.
3. Replace the placeholder values with your specific database credentials and secret keys.
