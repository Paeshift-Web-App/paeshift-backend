Open the terminal and proceed with the commands below:

1.  python -m venv venv (or python -m venv env)(creates the virtual environment)
2.  venv\Scripts\activate    (activates the virtual environment)
    #when done working always close your virtual environment by 
    # deactivate command
3.   pip install django      
4.   django-admin startproject payshift .     #create the app directly 
    #in the root directory 
    (ensure to add the dot after space)
        (creates django project, you can name the project anything)
5.  python manage.py runserver    
    (runs the server you can view on the browser, type localhost:8000)

5b. shut server down with ctrl + c
6.  python manage.py startapp frontend
        (creates the app within the django project, you can name the app anything)

.........................................................................................
-: The startproject command creates the following:


    manage.py 
    powerapp/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
-manage.py is A command-line utility that lets you interact with this Django 
    project in various ways.
-The  powerapp/ directory is the Python package for your project.
    Its used to from typing_extensions import Required
import anything inside it (e.g. powerapp.urls).
-powerapp/__init__.py is An empty file that tells Python that this 
    directory should be considered a Python package 
        (Do not tamper with this file, dont even open it)
-powerapp/settings.py: Settings/configuration for this Django project 
    will go here.
-powerapp/urls.py is The URL declarations for this Django project; 
    a 'table of contents' of your Django-powered site. 
-powerapp/asgi.py is An entry-point for ASGI-compatible web servers to
 serve your project.
    Asynchronous Server Gateway Interface designed to untie Channels 
    apps from a specific 
        application server and provide a common way to write application
         and middleware code.
            (Do not tamper with this file, dont even open it)
-powerapp/wsgi.py is An entry-point for WSGI-compatible web servers to 
serve your project. 
      Web Server Gateway Interface is Django's startproject management 
      command it sets up 
        a minimal default WSGI configuration for you, which you can tweak 
        as needed for 
        your project, and direct any WSGI-compliant application 
              server to use.
            (Do not tamper with this file, dont even open it)
-: The startapp command created the following:

firstapp/
      __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
This directory structure will house the firstapp application.
The moment the first app is created do the following:
..................................................................................



7. Open the powerapp/settings.py file:
 At the top of the file add:

 import os
 Then scroll to the Installed_Apps section to connect  
 the new app to the project

    INSTALLED_APPS = [.
    .
    .
    .
    .
    'firstapp.apps.FirstappConfig',
]
    Thereafter create media settings


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

8. -Next in the Project/urls.py, insert an include in the urlpatterns: 

from django.contrib import  admin
from django.urls import path, include 

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('firstapp.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




9 -: firstapp/views.py file:
from django.http import HttpResponse

# create your views 
def index(request):
    return HttpResponse("Hey Guys I am working with django now")
	# OR

def index(request):
    return render(request, 'index.html')

-create templates	 file - In appfile (create 'templates' add (index and base).html in it
	and 
create'static add img and css files in it' )


10. -: Next create a urls.py file inside the firstapp app and add:

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]



******** 
-Install pillow- (Picture)
 	pip install pillow
python -m pip install --upgrade pip
python -m pip install --upgrade Pillow

******** 


11. Create your project model:  

12. create Admin view:
How to get to the Admin site: 
First migrate the default django model:



13. -:      python manage.py makemigrations
13b. -:     python manage.py migrate
14. -:      python manage.py createsuperuser
	python manage.py migrate --run-syncdb

    Enter a username and press enter.
    -Username: xxxxxx
enter an email address and press enter:
    -Email address: admin@example.com

enter password and press enter:

    -Password: xxxxxx
    -Password (again): xxxxxxx
    

Things go well you will see...Superuser created successfully.

next :-     python manage.py runserver

15. -Next go to the browser type localhost:8000/admin enter. 
    when the admin site opens, enter your login details

16. Create views functions to query the db and send data to the template   

17. Display data on the template for your users.


So how do you work through an app?
The work flow is as below:
1. Install django and any other package needed for the app you want to build
2. Create your app model in models.py file 
3. Connect your model to the admin site through the admin.py file
4. Create django form should you need to collect data from your users
5. Define functions in views.py file to both query the db and persist data to the db   
6. Display data in the templates   
7. Happy coding ...


ORM : object-relational mapper



pip install django-mathfilters
pip install humanize
pip install requests


python -m pip install psycopg2

pip freeze>Requirements.txt
pip install -r requirements.tx
