fbauth
======

Requirements
============
* Django 1.6+

Installation
============
pip install django-fbauth-templatag

Testing
=======

You can try out fbauth using the installed demo included in the project. Just
run the `runserver` command to look at the demo.

Instructions
============
Load the `fbauth` template-tag library into your template, then call
`fbauth_css` inside your `head` tag and call the `fbauth_button` wherever you
want the Facebook button to be rendered.

E.g.

```django
{% load fbauth %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My App</title>
    {% fbauth_css %}
</head>
<body>
    {% fbauth_button %}
</body>
</html>
```

Configure the `FBAUTH_FACEBOOK_APP_ID` variable in you `settings` module with
you Facebook app ID.

Configure the `FBAUTH_REDIRECT_URL` variable in your `settings` module with the
url that should be receiving the access token from facebook. Sometimes it's more
convinient to put it inside the `__init__` module of your app so that you can
take advantage of Django's `reverse` function.

There's also a `FBAUTH_FACEBOOK_LOCALEL` variable which you can use to specify
an ISO-15897 (also know as POSIX locale) locale for the Facebook API. Users of
your project will see the Facebook UI translated in the locale you specify. The
default locale is `en_US`.

E.g.

```python
# demo/__init__.py
from django.core.urlresolvers import reverse
from django.conf import settings

setattr(settings, 'FBAUTH_REDIRECT_URL',
    reverse('demo:redirect') + '?access_token={0}')
```

Remember that your redirection URL should include the format token `{0}` to
indicate where Facebook's access token should be written.
