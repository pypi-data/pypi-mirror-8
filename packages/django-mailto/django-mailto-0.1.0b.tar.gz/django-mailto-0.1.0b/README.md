# django-mailto

django-mailto is a simple reusable Django app which enables you to send, manage and queue the sending of templated
and multilingual emails.

Queueing is an optional feature, which will be enabled when [celery - Distributed Task Queue](https://github.com/celery/celery) 
is up and running within your project.

## Dependencies

- [Django >= 1.4](https://www.djangoproject.com/)
- [Celery >= 3.0.0](http://www.celeryproject.org/) (optional)

## Features

- simple interface `mailto(['test@localhost'], 'test')`
- inline editing of HTML mails
- queueing
- Opt-In/-Out

## Getting started

1. `pip install django-mailto`

2. Add `mailto` to your `INSTALLED_APPS` settings:

    ```
    INSTALLED_APPS = (
        ...
        'mailto',
    )
    ```

3. And add it to your urls:

    ```
    urlpatterns += patterns('',
        url(r'^mailto/', include('mailto.urls')),
    )
    ```

4. Finally run `manage.py syncdb`.


## Usage

### `mailto(recipients, slug, language_code=settings.LANGUAGE_CODE, context={}, from_email=None, reply_to=None, cc=[], bcc=[], headers={}, attachments=[])`

Parameters:

- **recipients** (list) - A list of recipeint addresses.
- **slug** (string) - Slug of Mail object to be sent.
- **language_code** (string) - Language code.
- **context** (dict) - A dictionary of additional context.
- **from_email** (string) - Senders email address, will override `sender_email` attribute of an existing Mail object.
- **reply_to** (string) - Reply-To email address, will override `reply_to` attribute of an existing Mail object.
- **cc** (list) -  A list of recipient addresses., will extend `cc` attribute of an existing Mail object.
- **bcc** (list) - A list of recipient address, will extend `bcc` attribute of an existing Mail object.
- **headers** (dict) - A dictionary of extra headers to put on the message. The keys are the header name, values are the 
    header values. It’s up to the caller to ensure header names and values are in the correct format for an email message.
- **attachment** (list) - A list of attachments to put on the message. These can be either `email.MIMEBase.MIMEBase` instances, or 
    `(filename, content, mimetype)` triples.

```
from mailto import mailto

mailto(['test@localhost'], 'test')
```

In case, Mail object with given slug, does not exist, it will be created with `active=False`, without sending. In order
to provide an initial set of Mail objects specify `MAILTO_MAILS` setting in your settings file, which will be created on
`syncdb`.
 
### In your templates 

Load `mailtotags` into your template and define placeholders where content should be editable. An example minimal template
with a simple footer would look like this (e.g. `mailto/simple_footer.html`):

```
{% extends 'mailto/base.html' %}
{% load mailtotags %}

{% block title %}{{ block.super }}{% endblock %}
{% block extra_head %}{{ block.super }}{% endblock %}
{% block extra_body_attrs %}{{ block.super }}{% endblock %}

{% block body %}
        {% placeholder 'main-content' %}
        
        <hr>
        Thank you for treating this mail as confidential
{% endblock %}

{% block extra_body %}{{ block.super }}{% endblock %}
``` 

A coresponding plain text template would look like this (e.g. `mailto/simple_footer.txt`):

```
{{ body }}

---
Thank you for treating this mail as confidential.
```

### Template rendering

Template rendering  will be done with current `context_processor` setting in mind. This means, there is the same context
available as in regular views.
In case the recipients email address matches an existing user, than recipients User object will be add to `recipient`
context variable. E.g. `{{ recipient.username }}` will return the User objects username.

### Opt-out URL

To get the Opt-out URL for the current user use `{{ recipient.optin.get_optout_url }}`

## Settings

### MAILTO_TEMPLATES

django-mailto is shipped with a default set of email templates [thanks to *Antwort*](https://github.com/internations/antwort) but it
is easy to setup your own

Default:

```
(
    ('mailto/default.html', _('Default')),
    ('mailto/default_2col.html', _('Default 2 column')),
    ('mailto/default_3col.html', _('Default 3 column')),
)
```

Additionally when a `mailto/default.txt` is available besides the `mailto/default.html` it will be taken as template for 
plain body of your email.

### MAILTO_MAILS

Default: `None`

Profile an initial set of Mail objects by settings a list or tuple of mail slugs. They will be crated on each syncdb if 
not already existing.

```
(
    'mail-registration',
    'mail-password-reset',
)
```

### MAILTO_DEFAULT_SENDER_EMAIL

Default: `settings.DEFAULT_FROM_EMAIL`

Sets the default sender email for new Mail objects.

### MAILTO_OPTOUT_REDIRECT_URL

Default: `"/"`

After a successful Opt-out the user will be redirected to an URL of your choice.