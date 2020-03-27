###### Create the database and an admin user:

```
CREATE DATABASE sprigs;
CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE sprigs TO admin;
```

###### Clone the web app:
```
git clone https://github.com/ac-small/sprigs-webapp.git
cd sprigs-webapp
```

###### Modify db connection strings
Navigate to azuresite/settings.py
Change database connection strings if needed.

###### Activate virtual environment:
```
py -3 -m venv venv
venv\scripts\activate
```

###### Install required dependancies, and migrate db tables and static datasets.
```
pip install -r requirements.txt
python manage.py migrate
```

###### Scrape product information
```
python manage.py scrape_data
```

###### Run the app:
```
python manage.py runserver
```

###### Additional Help:
If you accidentally removed tables and need to rerun migration scripts:
```
python manage.py migrate --fake sprigs zero
python manage.py migrate sprigs
```
