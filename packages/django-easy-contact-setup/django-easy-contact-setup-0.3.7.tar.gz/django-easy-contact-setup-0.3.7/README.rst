
===========
Description
===========

This app is for usage with django-easy-contact. It allows setting up an 
mail form in the admin section. 

**License**

    New BSD license
    
**Notes**

    Tested with Django 1.2, 1.3

**Features**

    * Mail form setup in via administration interface.
    * All important data will be saved encrypted.


============
Installation
============

**Dependences**

    easy_install or pip will resolve all dependences automaticly.

    * django-easy-contact
    * This app
    * Django

**Installation**

    *Manual Installation*

        * Download the file and unzip it.
        * Copy the folder in your project root.

    *Installation with pip*

        * Type in your terminal:

        ::
        
        :~$ pip install django-easy-contact-setup


        * With pip you can also uninstall it:

        ::

        :~$ pip uninstall django-easy-contact-setup


=====
Setup
=====

    * Add "easy_contact-setup" to you installed apps in the settings file.
    * Run:

    ::

    :~$ python manage.py syncdb
    :~$ python manage.py runserver

=====
Usage
=====

Now you can setup your django-easy-contact app via the admin interface.

