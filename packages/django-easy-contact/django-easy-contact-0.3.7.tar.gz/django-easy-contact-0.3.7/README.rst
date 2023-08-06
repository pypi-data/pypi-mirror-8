
===========
Description
===========

A simple contact form application.

**License**

    New BSD license

**Notes**

    * It's tested with Django 1.2

========
Features
========

    * You can use ervery outsite email host (the application will auto configure itself).
    * You can clearly see from witch sender and domain the email was sent.
    * optionally it works together with django-easy-contact-setup.

**It lacks**

    * Any spam protection
    * Mail sending to more then one reciver.

============
Installation
============

**Dependences**

    * This app
    * Django itself

**Installation**

    *Manual Installation*

        * Download the file and unzip it.
        * Copy the folder in your project root.

    *Installation with pip*

        * Type in your terminal:

        ::
        
        :~$ pip install django-easy-contact


        * With pip you can also uninstall it:

        ::

        :~$ pip uninstall django-easy-contact

**test your installation**

    Go to console and type:

    ::

    :~$ python
    >>> import easy_contact
    >>> easy_contact.VERSION

=====
Setup
=====

    * Add "easy_contact" to you installed apps in the settings file.
    * Either install and configure django-contact-form-setup ...
    * or make sure that your mail server settings in settigs.py are correct:
        - DEFAULT_FROM_EMAIL
        - EMAIL_HOST
        - EMAIL_HOST_PASSWORD
        - EMAIL_HOST_USER
    * Add the following to your urls.py:
        -   (r'^feedback/', include('easy_contact.urls')),
    * Finally run:

    ::

    :~$ python manage.py syncdb
    :~$ python manage.py runserver

=====
Usage
=====

Open a Browser and go to "http://127.0.0.1:8000/feedback/contact/". That's all.

**Hints**

    * The mailform needs at minimum 5 words as input.
