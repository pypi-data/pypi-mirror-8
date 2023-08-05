django-dbmessages
=================

**Almost like django.contrib.messages,
but doesn't need request to message a user.**

In fact, django-dbmessages is but a very thin and simple layer
on top of Django's ``contrib.messages``.

To message a user, you simply create and save an instance
of provided ``Message`` model via shell, Django admin, or some other means.

``Message`` model has all the same attributes you'd normally pass
to ``contrib.messages`` (level, message, extra_tags),
and in addition a ForeignKey link to User model.

The next time given user appears on the site, middleware provided by dbmessages
checks if user has any messages for them, and adds them to request using regular
``contrib.messages`` API. Then it deletes those messages from the DB.
Simple as that.


Quick start
-----------

0. Make sure to enable Django's ``contrib.messages`` in your project
   (`check the docs <https://docs.djangoproject.com/en/1.4/ref/contrib/messages/#enabling-messages>`_).

1. Install ``django-dbmessages`` (it's on PyPI).

2. Add ``'dbmessages'`` to your INSTALLED_APPS
   and ``'dbmessages.middleware.DBMessageMiddleware'`` to MIDDLEWARE_CLASSES.

3. Synchronize (or migrate) the DB.

Now you can get into shell and address a message to yourself:

    >>> from dbmessages.models import Message
    >>> from django.contrib import messages
    >>> Message.objects.create(to_user=your_user, level=messages.INFO, message="Ahoy there")

Provided your front-end is integrated with Django's ``contrib.messages``,
you should see the "Ahoy there" message the next time you log in
under your account.
