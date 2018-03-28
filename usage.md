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

* Set permission and folder

```textmate
chmod -R 777 upload
chmod -R 777 media
chmod 777 debug.log
```

* Run `python manager.py runserver 0.0.0.0:9160`

* If we disable debug `static files` no longer working.

* using `thumbnail` for display image in content

```textmate
sudo apt-get install imagemagick
https://sorl-thumbnail.readthedocs.io/en/v12.3/examples.html
```

* Using math in template `https://stackoverflow.com/questions/6285327/how-to-do-math-in-a-django-template`

* Building a list in template `https://stackoverflow.com/questions/4395230/building-a-list-in-django-templates`

* Using `django-taggit` and `django-autocomplete-light v3`

```textmate
pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light

https://django-taggit.readthedocs.io/en/latest/admin.html

```
* Using `https://github.com/idlesign/django-siteprefs` for site configuration

* How to customize third-party packages

Step 1 : Fork this package from github.com

Step 2 : 
```textmate
cd /var/www/html/package_django
git clone git@github.com:thienkimlove/django-constance.git

#change code and commit to our github and run:

pip install -e git+git://github.com/thienkimlove/django-constance.git#egg=django-constance --upgrade

# check if code change at

~/Env/tracuu/lib/python3.5/site-packages/constance/templates/admin/constance
```

Step 3 : RUn `pip freeze > requirements.txt` and we will see in `requirements.txt`

```textmate
-e git://github.com/thienkimlove/django-constance.git@4ee9981bfcbe5e7423fe65eb128e1485c27b73f8#egg=django_constance
```

* Deploy 

```textmate
mkdir -p /var/www/html/tracuu
CREATE DATABASE python_tracuu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mkvirtualenv tracuu
pip install -r requirements.txt
ln -s /var/www/html/tracuu/deploy/tracuu.ini /etc/uwsgi/sites/tracuu.ini
ln -s /var/www/html/tracuu/deploy/tracuuduoclieu.vn /etc/nginx/sites-enabled/tracuuduoclieu.vn
oot@ubuntu:/var/www/html/tracuu# chmod -R 777 files
(tracuu) root@ubuntu:/var/www/html/tracuu# chmod -R 777 upload/
(tracuu) root@ubuntu:/var/www/html/tracuu# chmod -R 777 media/
(tracuu) root@ubuntu:/var/www/html/tracuu# chmod -R 777 debug.log 
```