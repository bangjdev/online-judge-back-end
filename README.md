# LQDOJ's back-end

## First time clone

### 1. Install all requirement packages:
In Windows:
```bash
python -m pip install -r dependencies.txt
```
In Ubuntu:
```bash
sudo python3 -m pip install -r dependencies.txt
```
### 2. Migrate db
Run:
```bash
sudo python3 manage.py migrate --run-syncdb
```

## Usage
To create superuser account, run:
```bash
sudo python3 manage.py createsuperuser
```
To run in th development server:
```bash
sudo python3 manage.py runserver 0.0.0.0:8000
```

Make sure you can access the admin page at:
```url
localhost:8000/admin
```

## Dependencies:
This backend server uses celery and redis for the distributed async task queue, so you will need to
install and configurate theses settings properly.
