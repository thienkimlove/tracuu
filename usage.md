#### Setting projects

* Edit `core/models.py`
* Edit `core/forms.py`
* Edit `core/admin.py`
* Edit `project/settings.py` to change `database`
* Run commandline for create database

```textmate
mysql -uroot -ptieungao -e "CREATE DATABASE tracuu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

```

* Create virtualenv 

```textmate
mkvirtualenv tracuu
pip install -r requirements.txt
```
* Run migrate

```textmate
python manager.py makemigrations
python manager.py migrate
python manage.py createsuperuser
```
* Create message in Vi

```textmate
django-admin makemessages -l en
django-admin makemessages -l vi
```

Go to `core/locale/vi/LC_MESSAGES` to edit `django.po` and run `django-admin compilemessages`

