### New project settings


* Run command at first time

```textmate
mkvirtualenv duoclieu
pip3 install Django
pip3 install mysqlclient
cd /var/www/html
django-admin startproject site
cd site
django-admin startapp core
touch core/urls.py
django-admin startapp frontend
touch frontend/urls.py
touch debug.log
touch readme.md
mkdir -p static
mkdir -p media
mkdir -p templates/admin
chmod -R 777 static
chmod -R 777 media

```
* Edit `site/settings.py`


```textmate

'DIRS': [os.path.join(BASE_DIR, 'templates')],

 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'python_site',
         'USER': 'root',
         'PASSWORD': 'tieungao',
         'HOST': '127.0.0.1',
         'PORT': '3306',
         'OPTIONS' : {
             'charset': 'utf8mb4',
         }
     }
 }
 
 LOGGING = {
     'version': 1,
     'disable_existing_loggers': False,
     'handlers': {
         'file': {
             'level': 'DEBUG',
             'class': 'logging.FileHandler',
             'filename': os.path.join(BASE_DIR, 'debug.log'),
         },
     },
     'loggers': {
         'django': {
             'handlers': ['file'],
             'level': 'DEBUG',
             'propagate': True,
         },
     },
 }
 LANGUAGE_CODE = 'en-us' 
 TIME_ZONE = 'Asia/Ho_Chi_Minh' 
 USE_I18N = True 
 USE_L10N = True 
 USE_TZ = True 
 STATIC_URL = '/static/' 
 MEDIA_URL = '/media/' 
 STATIC_ROOT = os.path.join(BASE_DIR, "static/")
 MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
 
```

* Add `frontend` and `core` to `INSTALLED_APPS`


*  Run migration `python3 manage.py migrate`

*  Create super user `python3 manage.py createsuperuser`

* Start `python3 manage.py runserver 0.0.0.0:9160`

* Access `http://192.168.99.100:9160/admin/`

#### Customize Django Admin templates.

Please see in `settings.py` we have :

```textmate
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```
Mean that we can copy the django admin templates and override this.


* Check where is django code `python -c "import django; print(django.__path__)"`

* Normally it should be `cd /root/Env/duoclieu/lib/python3.5/site-packages/django`

* Copy `cp contrib/admin/templates/admin/base_site.html /var/www/html/site/templates/admin/base_site.html`

* Edit this template file.

#### Working with apps

* Edit `site/urls.py`

```textmate
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('core/', include('core.urls')),
    url(r'^', include('frontend.urls')),
]
```

* Create Home page `mkdir -p frontend/templates/frontend`

`touch frontend/templates/frontend/homepage.html` 

and put content `Frontend Index`

* Edit `frontend/urls.py`

```textmate
from django.conf.urls import url
from django.views.generic import TemplateView

app_name = "frontend"

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="frontend/homepage.html"), name='homepage'),
]
```

* Create templates `mkdir -p core/templates/core`

* Edit `models.py`

Add init class for compatible with `Laravel` databases

```textmate
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
```

* Create First model

```textmate
class Position(TimeStampedModel):
    name = models.CharField(max_length=191, unique=True)
    def __str__(self):
        return "{0}".format(self.name)
    def get_absolute_url(self):
        pass
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Vị trí Banner"
        verbose_name_plural = "positions"
```

After create models , run 

```textmate
python manage.py makemigrations
python manage.py migrate
``` 

* Note 

- If have error with unicode `1366 mysql` then we need to fix `utf8mb4` problem.

- If have any error with migration reset migration for `core` app `python manage.py migrate core zero`

* Make models show in Admin

```textmate
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ["name"]
    ordering = ["name"]
    
admin.site.register(Position, PositionAdmin)
```
* Translation 

```textmate
https://docs.djangoproject.com/en/2.0/topics/i18n/translation/
```

First in every place in our code we must using

```textmate
# in code

from django.utils.translation import gettext_lazy as _

verbose_name = _("Positions")
verbose_name_plural = _("Positions")

#in template

<title>{% trans "This is the title." %}</title>
<title>{% trans myvar %}</title>

{% blocktrans %}This string will have {{ value }} inside.{% endblocktrans %}

{% some_tag _("Page not found") value|yesno:_("yes,no") %}

```

Second, using commandline

```textmate
apt-get install gettext
mkdir -p core/locale
mkdir locale
mkdir -p frontend/locale
```

Check setting in `site/settings.py`

Note about `LANGUAGE_CODE` :

```textmate
LANGUAGE_CODE
Default: 'en-us'

A string representing the language code for this installation. This should be in standard language ID format. For example, U.S. English is "en-us". See also the list of language identifiers and Internationalization and localization.

USE_I18N must be active for this setting to have any effect.

It serves two purposes:

If the locale middleware isn’t in use, it decides which translation is served to all users.
If the locale middleware is active, it provides a fallback language in case the user’s preferred language can’t be determined or is not supported by the website. It also provides the fallback translation when a translation for a given literal doesn’t exist for the user’s preferred language.
```

```textmate
LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'vi'
```

Please check the list of languages `http://www.i18nguy.com/unicode/language-identifiers.html`


Next run 

```textmate
django-admin makemessages -l en
django-admin makemessages -l vi
```

Go to `core/locale/vi/LC_MESSAGES` to edit `django.po` and run `django-admin compilemessages`

* Add a new page to Django Admin Model

```textmate
https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls
```

* Customize Admin Page

```textmate
 List views: 
     Add additional fields/information displayed for each record. 
     Add filters to select which records are listed, based on date or some other selection value (e.g. Book loan status).
     Add additional options to the actions menu in list views and choose where this menu is displayed on the form.
 Detail views
     Choose which fields to display (or exclude), along with their order, grouping, whether they are editable, the widget used, orientation etc.
     Add related fields to a record to allow inline editing (e.g. add the ability to add and edit book records while you're creating their author record).
```
* Reversing admin URLs

```textmate
Index	index	 
Login	login	 
Logout	logout	 
Password change	password_change	 
Password change done	password_change_done	 
i18n JavaScript	jsi18n	 
Application index page	app_list	app_label
Redirect to object’s page	view_on_site	content_type_id, object_id
Each ModelAdmin instance provides an additional set of named URLs:

Page	URL name	Parameters
Changelist	{{ app_label }}_{{ model_name }}_changelist	 
Add	{{ app_label }}_{{ model_name }}_add	 
History	{{ app_label }}_{{ model_name }}_history	object_id
Delete	{{ app_label }}_{{ model_name }}_delete	object_id
Change	{{ app_label }}_{{ model_name }}_change	object_id
The UserAdmin provides a named URL:

Page	URL name	Parameters
Password change	auth_user_password_change	user_id
These named URLs are registered with the application namespace admin, and with an instance namespace corresponding to the name of the Site instance.

So - if you wanted to get a reference to the Change view for a particular Choice object (from the polls application) in the default admin, you would call:

>>> from django.urls import reverse
>>> c = Choice.objects.get(...)
>>> change_url = reverse('admin:polls_choice_change', args=(c.id,))
This will find the first registered instance of the admin application (whatever the instance name), and resolve to the view for changing poll.Choice instances in that instance.

If you want to find a URL in a specific admin instance, provide the name of that instance as a current_app hint to the reverse call. For example, if you specifically wanted the admin view from the admin instance named custom, you would need to call:

>>> change_url = reverse('admin:polls_choice_change', args=(c.id,), current_app='custom')
For more details, see the documentation on reversing namespaced URLs.

To allow easier reversing of the admin urls in templates, Django provides an admin_urlname filter which takes an action as argument:

{% load admin_urls %}
<a href="{% url opts|admin_urlname:'add' %}">Add user</a>
<a href="{% url opts|admin_urlname:'delete' user.pk %}">Delete this user</a>
The action in the examples above match the last part of the URL names for ModelAdmin instances described above. The opts variable can be any object which has an app_label and model_name attributes and is usually supplied by the admin views for the current model.
```
* Overriding vs. replacing an admin template

  Because of the modular design of the admin templates, it is usually neither necessary nor advisable to replace an entire template. It is almost always better to override only the section of the template which you need to change.
  
  To continue the example above, we want to add a new link next to the History tool for the Page model. After looking at `change_form.html` we determine that we only need to override the `object-tools-items` block. Therefore here is our new `change_form.html` :
```textmate
{% extends "admin/change_form.html" %}
{% load i18n admin_urls %}
{% block object-tools-items %}
    <li>
        <a href="{% url opts|admin_urlname:'history' original.pk|admin_urlquote %}" class="historylink">{% trans "History" %}</a>
    </li>
    <li>
        <a href="mylink/" class="historylink">My Link</a>
    </li>
    {% if has_absolute_url %}
        <li>
            <a href="{% url 'admin:view_on_site' content_type_id original.pk %}" class="viewsitelink">{% trans "View on site" %}</a>
        </li>
    {% endif %}
{% endblock %}
```

And that’s it! If we placed this file in the `templates/admin/my_app` directory, our link would appear on the change form for all models within `my_app`.

* Templates which may be overridden per app or model
Not every template in `contrib/admin/templates/admin` may be overridden per app or per model. The following can:

```textmate
app_index.html
change_form.html
change_list.html
delete_confirmation.html
object_history.html
popup_response.html
```

For those templates that cannot be overridden in this way, you may still override them for your entire project. Just place the new version in your `templates/admin` directory. This is particularly useful to create custom 404 and 500 pages.

Note

Some of the admin templates, such as `change_list_results.html` are used to render custom inclusion tags. These may be overridden, but in such cases you are probably better off creating your own version of the tag in question and giving it a different name. That way you can use it selectively.

* Root and login templates
If you wish to change the index, login or logout templates, you are better off creating your own AdminSite instance (see below), and changing the `AdminSite.index_template` , `AdminSite.login_template` or `AdminSite.logout_template` properties.

#### Start working with `Banners`

*  Create new models

```textmate
pip install Pillow
python manage.py makemigrations
python manage.py migrate
```

* Working with Editor

We have 2 ways to work with HTML editor in django 2.0

- Using `TinyMCE` download at `https://www.tinymce.com/download/` and `https://github.com/smacker/django-filebrowser-no-grappelli`

Step to working with it

```textmate
pip install -e git+git://github.com/smacker/django-filebrowser-no-grappelli.git#egg=django-filebrowser
mkdir -p core/static/core/js
#download tinymce
# create tiny.js with content
# Extend template at core/templates/admin/core/change_form.html
```

- Using django CKEditor at `https://github.com/django-ckeditor/django-ckeditor`

* For development when testing with `media` and `static` we need to add to `urls.py` as below 

```textmate
urlpatterns = [
    url(r'^admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    #path('core/', include('core.urls')),
    url(r'^', include('frontend.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

* Add new view to admin model page

First we need create `core/templates/core/testing.html`

Second we add to `PositionAdmin` class in `admin.py`

```textmate
# add new url which can access through /admin/myapp/mymodel/my_view/
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('testing/', self.admin_site.admin_view(self.testing))
        ]
        return my_urls + urls
    def testing(self, request):
        # ...
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            test="Value from View",
        )
        return TemplateResponse(request, "core/testing.html", context)
```

Now we can access this new page through url `/admin/core/position/testing/`

* Admin Django Urls list `https://docs.djangoproject.com/en/dev/ref/contrib/admin/#admin-reverse-urls`

```textmate
Index	index	 
Login	login	 
Logout	logout	 
Password change	password_change	 
Password change done	password_change_done	 
i18n JavaScript	jsi18n	 
Application index page	app_list	app_label
Redirect to object’s page	view_on_site	content_type_id, object_id
Each ModelAdmin instance provides an additional set of named URLs:

Page	URL name	Parameters
Changelist	{{ app_label }}_{{ model_name }}_changelist	 
Add	{{ app_label }}_{{ model_name }}_add	 
History	{{ app_label }}_{{ model_name }}_history	object_id
Delete	{{ app_label }}_{{ model_name }}_delete	object_id
Change	{{ app_label }}_{{ model_name }}_change	object_id
The UserAdmin provides a named URL:

Page	URL name	Parameters
Password change	auth_user_password_change	user_id

#Template
{% load admin_urls %}
<a href="{% url opts|admin_urlname:'add' %}">Add user</a>
<a href="{% url opts|admin_urlname:'delete' user.pk %}">Delete this user</a>
# INcode

change_url = reverse('admin:polls_choice_change', args=(c.id,))
#If using adminSite name custom
 change_url = reverse('admin:polls_choice_change', args=(c.id,), current_app='custom')
```

Check example in `core/templates/core/testing.html`

* Full Example about Django get data from DB and show in templates:

`https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views`

* Show log entries in Admin `pip install git+git://github.com/yprez/django-logentry-admin@fix-admin-links#egg=django-logentry-admin`

#### Permission

* Define permissions and custom permissions in model

```textmate
class Store(models.Model):
    name = models.CharField(max_length=30)    
    address = models.CharField(max_length=30,unique=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    class Meta:
        default_permissions = ('add',)
        permissions = (('give_refund','Can refund customers'),('can_hire','Can hire employees'))
```

* Check permission in view we using 

```textmate
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('polls.can_vote', raise_exception=True)
def my_view(request):
```

Or something more details

```textmate
# Method check to see if User belongs to group called 'Barista'
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

@user_passes_test(lambda u: Group.objects.get(name='Baristas') in u.groups.all())
def dashboard(request):
    # Logic for dashboard

# Explicit method check, if User is authenticated and has permissions to change Store model
# Explicit method with test
def user_of_stores(user):
    if user.is_authenticated() and user.has_perm("stores.change_store"):
        return True
    else:
        return False

# Method check using method
@user_passes_test(user_of_stores)
def store_manager(request):
    # Logic for store_manager

# Method check to see if User has permissions to add Store model
from django.contrib.auth.decorators import permission_required

@permission_required('stores.add_store')
def store_creator(request):
    # Logic for store_creator
```


or with class view

```textmate
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = 'polls.can_vote'
    # Or multiple of permissions:
    permission_required = ('polls.can_open', 'polls.can_edit')
```

In Template

```textmate
  {% if perms.core.add_banner %}
  
  Just like the has_perm() method, permission names take the form "<app label>.<permission codename>" (i.e. polls.can_vote for a permission on a model in the polls application).
  
   {% if user.is_authenticated %}
            {#  Content for authenticated users  #}
         {% endif %}
         
         {% if perms.stores.add_store %}
            {#  Content for users that can add stores #}
         {% endif %}
         
         {% for group in user.groups.all %}
            {% if group.name == 'Baristas'  %}
                 {# Content for users with 'Baristas' group #}
            {% endif %}
         {% endfor %}
  
```

* For custom check we using `user_passes_test`

```textmate
from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('@example.com')

@user_passes_test(email_check)
def my_view(request):

@user_passes_test(email_check, login_url='/login/')
def my_view(request):

from django.contrib.auth.mixins import UserPassesTestMixin

class MyView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.email.endswith('@example.com')
        
class TestMixin1(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.email.endswith('@example.com')

class TestMixin2(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.username.startswith('django')

class MyView(TestMixin1, TestMixin2, View):        

```

* Custom permissions
To create custom permissions for a given model object, use the permissions model Meta attribute.

This example Task model creates three custom permissions, i.e., actions users can or cannot do with Task instances, specific to your application:

```textmate
class Task(models.Model):
    ...
    class Meta:
        permissions = (
            ("view_task", "Can see available tasks"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
```
The only thing this does is create those extra permissions when you run `manage.py migrate` (the function that creates permissions is connected to the `post_migrate` signal). Your code is in charge of checking the value of these permissions when a user is trying to access the functionality provided by the application (`viewing tasks`, `changing the status of tasks`, `closing tasks`.) Continuing the above example, the following checks if a user may view tasks:

`user.has_perm('app.view_task')`

#### Best about Django ORM query `https://www.webforefront.com/django/multiplemodelrecords.html`


#### Logging `https://lincolnloop.com/blog/django-logging-right-way/`

Using debug toolbar

```textmate
http://www.bedjango.com/blog/how-install-django-debug-toolbar/
```
### Working with transfer database from old

* Read more about `https://docs.djangoproject.com/en/2.0/topics/db/sql/`

`To protect against SQL injection, you must not include quotes around the %s placeholders in the SQL string.`

* With Raw SQL using `MysqlDB` package we can using as below to make `cursor.fetchall()` return a list

```textmate
conn = MySQLdb.connect(host="42.112.31.173",    # your host, usually localhost
           user="tieungao",         # your username
           passwd="tieungao123",  # your password
           db=db_name, charset='utf8mb4')        # name of the database
           
cursor = conn.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("select * from %s" % table)
model_name.objects.bulk_create([model_name(**row) for row in cursor.fetchall()])           
```

Will return output as 

```textmate
[{'parent_id': None, 'id': 54360982}, {'parent_id': None, 'id': 54360880}]
```

* With Django Raw SQL we have 2 functions as below:

```textmate
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]    
```

which return as below

```textmate
>>> cursor.execute("SELECT id, parent_id FROM test LIMIT 2");
>>> cursor.fetchall()
((54360982, None), (54360880, None))

>>> cursor.execute("SELECT id, parent_id FROM test LIMIT 2");
>>> dictfetchall(cursor)
[{'parent_id': None, 'id': 54360982}, {'parent_id': None, 'id': 54360880}]

>>> cursor.execute("SELECT id, parent_id FROM test LIMIT 2");
>>> results = namedtuplefetchall(cursor)
>>> results
[Result(id=54360982, parent_id=None), Result(id=54360880, parent_id=None)]
>>> results[0].id
54360982
>>> results[0][0]
54360982
```

* Working with JSON Field Django

- Loop over dict Python 3
```textmate
will simply loop over the keys in the dictionary, rather than the keys and values. To loop over both key and value you can use the following:

For Python 2.x:

for key, value in d.iteritems():
For Python 3.x:

for key, value in d.items():
```
- Error `TypeError: Can't convert 'NoneType' object to str implicitly`

solve by using `str(obj)`

- We using `https://github.com/irothschild/simple-json-text-field` for convert textfield to Dict when get from database.

- But come with another complete solution as below

```textmate
# For model field
https://github.com/dmkoch/django-jsonfield
# For display in Admin form
https://github.com/nnseva/django-jsoneditor
```

- Please check the source above for how to build custom widget and custom field django

`http://andrearobertson.com/blog/2017/06/17/django-example-creating-a-custom-form-field-widget/`
`https://www.webforefront.com/django/formcustomfieldsandwidgets.html`

* Select 2 widget

```textmate
http://django-select2.readthedocs.io/en/latest/django_select2.html
https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_tag', 'views', 'get_modules', 'get_tags', 'created_at', 'status')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('views', 'user')
    search_fields = ['title']
    list_filter = (
        'category',
        'status',
    )
    form = PostForm
    autocomplete_fields = ['category', 'tag', 'module']
```

* Count and condition through many relationship we must using

```textmate
https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
provinces = Province.objects.annotate(num_stores=Count('district__store')).filter(num_stores__gt=0)
```

I used that for create custom filter in django admin list.

* For export and import in admin using 

```textmate
https://django-import-export.readthedocs.io/en/latest/api_admin.html
http://django-import-export.readthedocs.io/en/latest/getting_started.html

Unlike specifying a related field in your resource like so…

class Meta:
    fields = ('author__name',)
…using a ForeignKeyWidget has the advantage that it can not only be used for exporting, but also importing data with foreign key relationships.

http://django-import-export.readthedocs.io/en/latest/api_widgets.html#import_export.widgets.ForeignKeyWidget

```

### Working with Frontend.

* Copy `CSS/HTML` materials to `frontend/static/frontend`

* SEO packages

From `http://libi.geex-arts.com/libraries?search=SEO&ordering=-likes_count&tags=169`

we get updated version of Django-SEO which is no longer maintain

```textmate
pip install django-seo2
#added djangoseo to your INSTALLED_APPS setting

```
