====================
django-trello-broker
====================
:Info: Django app to integrate BitBucket POST hooks and Trello boards
:Version: 0.1
:Author: Peter Sanchez <peter@netlandish.com> - Netlandish Inc. (http://www.netlandish.com)

Dependencies
============

* Python 2.7+
* Django 1.7+
* trello 0.9.1+
* requests 2.2.1+


Installation
============

PIP::

    pip install django-trello-broker

Basic Manual Install::

    $ python setup.py build
    $ sudo python setup.py install

Alternative Install (Manually):

| Place trello_broker directory in your Python path. Either in your Python installs site-packages directory or set your $PYTHONPATH environment variable to include a directory where the webutils directory lives.


Usage
=====

#. Add 'trello_broker' to your INSTALLED_APPS

#. Add 'trello_broker.urls' somewhere in your url structure. Example::

    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^broker', include('trello_broker.urls')),
        ... (all your other urls here) ...
    )

#. Add at least 1 Trello Token to the database. Example::

    $ ./manage.py add_trello_token
    Enter your Trello applications name.

    App Name: Netlandish Bot

    Enter your Trello user API Key. You can get it from:

    https://trello.com/1/appKey/generate

    API Key: <Our Super Secret Key Here>

    Go to the following URL to get your API Token:

    https://trello.com/1/authorize?key=<Our Super Secret Key Here>&name=Netlandish+Bot&expiration=never&response_type=token&scope=read,write

    API Token: <Our Super Secret Token Here>
    Saved token (ID: 1) to the database.

#. Now you can automatically populate all Trello boards the new token has access to. Example::

    $ ./manage.py populate_trello_boards
    Processing token Netlandish Bot
    Processing board BracketWire Development
    Processing board Bracketwire Planning
    Processing board CHAP Development
    Processing board CHAP Planning
    Processing board CartFreak Development
    Processing board CartFreak Planning
    .......

#. Go to http://yourdomain.com/admin/ (or your admin URL) and add BitBucket Repositories. After saving you'll be able to add a new "Rule". Once you save that rule, you'll be able to add another. Currently there are only 2 rules allowed. "Referenced" and "Fixes / Closes".

  **Referenced**
    When a card has been referenced in a commit message, this rule will be triggered.

  Example
    Simply using "#<card-short-id>" works. For instance, "Starting working on new feature for #213"


  **Fixes / Closes**
    When a card has been referenced in a commit message but also uses a "fix" or "close" prefix

  Example:
    One of the following words following by the card short ID. Words are "fix(ed|es)" or "close(d|s)". This is case insensitive. For instance, "Finished work for new feature. Closes #213"

  .. image:: http://all-media.s3.amazonaws.com/images/broker_admin.png
     :align: center
     :width: 1000px
     :height: 575px
     :target: http://all-media.s3.amazonaws.com/images/broker_admin.png

#. Add the post hook to your BitBucket repository settings. See `BitBucket POST
Hook Management <https://confluence.atlassian.com/display/BITBUCKET/POST+hook+management?continue=https%3A%2F%2Fconfluence.atlassian.com%2Fdisplay%2FBITBUCKET%2FPOST%2Bhook%2Bmanagement&application=cac>`_

  *Note* Be sure to include the access_key if you stored one in your BitBucket Repo in the Django Admin. For instance, if you used "foobar" as your access key in Django admin, in the BitBucket settings you need to pass in the access key like so: http://yourdomain.com/broker/?access_key=foobar


Settings
========

There are a few settings that the application supports.

#. TRELLO_BROKER_USE_CELERY - Defaults to False. If True, the broker processor will use the celery task "celery_process_commits" which is simply a wrapper for the normal "process_commits" function to run via your celery setup.

#. TRELLO_BROKER_RESTRICT_IPS - Defaults to False. If True, the broker will check that the client sending the request comes from the specified BitBucket broker servers. See: `BitBucket IP List Here <https://confluence.atlassian.com/display/BITBUCKET/What+are+the+Bitbucket+IP+addresses+I+should+use+to+configure+my+corporate+firewall>`_

#. TRELLO_BROKER_BITBUCKET_IPS - A list of client IP's that are allowed to POST to the broker. Default's to ::

    ['131.103.20.165', '131.103.20.166']

   This setting depends on TRELLO_BROKER_RESTRICT_IPS being set to True


Admin Actions
=============

Also included is a simple Admin Action that makes it easy for you to re-populate one, or many, of your Trello boards via the Admin list page. Just select the boards you want to update, select the action, hit "Go".

  .. image:: http://all-media.s3.amazonaws.com/images/broker_actions.png
     :align: center
     :width: 1000px
     :height: 229px
     :target: http://all-media.s3.amazonaws.com/images/broker_actions.png

==================
Commercial Support
==================

This software, and lots of other software like it, has been built in support of many of
Netlandish's own projects, and the projects of our clients. We would love to help you 
on your next project so get in touch by dropping us a note at hello@netlandish.com.
