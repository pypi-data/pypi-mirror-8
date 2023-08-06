================
Django Users API
================

.. image:: https://travis-ci.org/mohabusama/django-users-api.svg?branch=master
    :target: https://travis-ci.org/mohabusama/django-users-api


Django users RESTful API using `Tastypie <https://django-tastypie.readthedocs.org/en/latest/toc.html>`_. This django app provides RESTful interface to:

- `Django User <https://docs.djangoproject.com/en/1.6/topics/auth/default/#user-objects>`_
- `Django Group <https://docs.djangoproject.com/en/1.6/topics/auth/default/#groups>`_
- `Django Permission <https://docs.djangoproject.com/en/1.6/topics/auth/default/#permissions-and-authorization>`_


Install
=======

::

    pip install django-users-api


or from cloned repo

::

    python setup.py install


Development
===========

Run tests:

::

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py test


Integration
===========

You can integrate **django-users-api** app within your django app in various ways.

URLConfig (default)
-------------------

Add **django-users-api** default urls to your projects urls. In the following example, we will include our *users_api.urls* prefixed with 'auth/'.

In project urls.py:

::

    from django.conf.urls import patterns, include, url

    urlpatterns = patterns(
        '',
        # ...,
        url(r'^auth/', include('users_api.urls')),
        # ...
    )

The **users_api** URLs will be accessible via:

::

    /auth/users/
    /auth/groups/
    /auth/permissions/
    ...

Selected Resources
------------------

In some cases you might need to exclude some resources from your project urls. In this case you will have to add the *required* resource(s) yourself.

Assuming you only require the **UsersResource** to be available (i.e. excluding **GroupsResource** & **PermissionsResource**)

In project urls.py:

::

    from django.conf.urls import patterns, include, url

    from users_api.common import UsersApi
    from users_api.api.users import UsersResource

    django_users_api = UsersApi()
    django_users_api.register(UsersResource())

    urlpatterns = patterns(
        '',
        # ...
        url(r'', include(django_users_api.urls)),
        # ...
    )

The **UsersResource** url will be accessible via:

::

    /users/


Resources
=========

UsersResource
-------------

A tastypie ModelResource for **django.contrib.auth.models.User**.

**GET**

- List all users: ``/users/``
- List user 1: ``/users/1/``

User JSON response example:

::

    {
        "dateJoined": "2014-12-24T13:04:36",
        "email": "admin@admin.com",
        "firstName": "",
        "isActive": true,
        "isStaff": true,
        "isSuperuser": true,
        "lastLogin": "2015-01-03T14:19:41.060600",
        "lastName": "",
        "resourceUri": "/users/1/",
        "username": "admin"
    }

**POST**

- Create new user: ``/users/``

*Important*: Creating user requires a **password** field to be submitted with data.

User JSON request payload example:

::

    {
        "email": "new-user@admin.com",
        "firstName": "New",
        "lastName": "User",
        "username": "new_user"
        "password": "us3rP@sswd"
    }

**PUT**

- Update existing user: ``/users/1/``

Submitting password field will change the user password.

**DELETE**

- Delete existing user: ``/users/2/``

GroupsResource
--------------

A tastypie ModelResource for **django.contrib.auth.models.Group**.

**GET**

- List all groups: ``/groups/``
- List group 1: ``/groups/1/``
- List user 1 groups: ``/users/1/groups/``

Group JSON response example:

::

    {
        "name": "Group name",
        "resourceUri": "/groups/1/"
    }

**POST**

- Create new group: ``/groups/``

Group JSON request payload example:

::

    {
        "name": "HR Group"
    }

**PUT**

- Update existing group: ``/groups/1/``
- Assign group 1 to user 1: ``/users/1/groups/1/``

**DELETE**

- Delete existing group: ``/groups/2/``
- Remove group 1 from user 1: ``/users/1/groups/1/``

PermissionsResource
-------------------

A tastypie ModelResource for **django.contrib.auth.models.Permission**.

**GET**

- List all permissions: ``/permissions/``
- List permission 1: ``/permissions/1/``
- List user 1 permissions: ``/users/1/permissions/``
- List group 1 permissions: ``/groups/1/permissions/``

Permission JSON response example:

::

    {
        "codename": "add_logentry",
        "contentTypeUri": "/contenttypes/1/",
        "name": "Can add log entry",
        "resourceUri": "/permissions/1/"
    }

**POST**

- Create new permission: ``/permissions/``

*Important*: A valid permission should reference a valid ContentType via *contentTypeUri* field (see `ContentTypesResource`_).

Permission JSON request payload example (assuming we have a *Blog* model):

::

    {
        "codename": "add_blog",
        "contentTypeUri": "/contenttypes/20/",
        "name": "Can add new blog",
    }

**PUT**

- Update existing permission: ``/permissions/1/``
- Assign permission 1 to user 1: ``/users/1/permissions/1/``
- Assign permission 1 to group 1: ``/groups/1/permissions/1/``

**DELETE**

- Delete existing permission: ``/permissions/2/``
- Remove permission 1 from user 1: ``/users/1/permissions/1/``
- Remove permission 1 from group 1: ``/groups/1/permissions/1/``

ContentTypesResource
--------------------

A Read-only tastypie ModelResource for **django.contrib.auth.models.ContentType**.

**GET**

- List all contenttypes: ``/contenttypes/``
- List contenttype 1: ``/contenttypes/1/``

ContentType JSON response example:

::

    {
        "appLabel": "admin",
        "model": "logentry",
        "name": "log entry",
        "resourceUri": "/contenttypes/1/"
    }


Authentication
==============

By default, all resources use Tastypie `SessionAuthentication <https://django-tastypie.readthedocs.org/en/latest/authentication.html#sessionauthentication>`_.


Authorization
=============

By default, all resources use Tastypie `DjangoAuthorization <https://django-tastypie.readthedocs.org/en/latest/authorization.html#djangoauthorization>`_.

*Important*: DjangoAuthorization gives *Read access* to all users, which might not be the desired behavior.


Extend
======

Django-users-api resources are based on Tastypie `ModelResource class <https://django-tastypie.readthedocs.org/en/latest/resources.html#why-class-based>`_, which gives you the ability to extend and override any of the *users_api* resources.


License
=======

`MIT License <https://github.com/mohabusama/django-users-api/blob/master/LICENSE>`_.
