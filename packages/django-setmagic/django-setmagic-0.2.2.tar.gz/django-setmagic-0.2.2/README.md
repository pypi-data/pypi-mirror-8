# django-setmagic

Magically editable settings for winged pony lovers.


## Why?

Because sometimes it's cool to set global configuration values through a nice
interface on the Django admin. And that's what SetMagic make possible. Enjoy!


## Install and set up

Install it into your project's virtual environment:

	$ pip install django-setmagic

Make sure you already have the [Django admin][1] set up! Then append to your
Django project's `INSTALLED_APPS` setting.

	INSTALLED_APPS = [
		...
		'django.contrib.admin',
		'setmagic',
		...
	]

Also enable the SetMagic template context processor, if you want to use it on
your templates, by adding it to the `TEMPLATE_CONTEXT_PROCESSORS` list:

	TEMPLATE_CONTEXT_PROCESSORS = [
		...
		'setmagic.context_processors.load_setmagic',
	]

Create the necessary tables, like usual:

	$ python manage.py syncdb

...and that's pretty much it. :)


## Usage

SetMagic will look into your project's settings for the name `SETMAGIC_SCHEMA`.
It should be defined as a pure Python list of groups like the example below:

	SETMAGIC_SCHEMA = [
	    ('Facebook App Credentials', [
	        dict(
	            name='FACEBOOK_APP_ID',
	            label=u'Facebook app ID',
	            help_text=u'Unique app identification code provided by Facebook.'),
	        dict(
	            name='FACEBOOK_APP_SECRET',
	            label=u'Facebook API secret',
	            help_text=u'Unique and secret API code provided by Facebook.'),
	    ]),
	    ('Tracking', [
	        dict(
	            name='GOOGLE_ANALYTICS_CODE',
	            label=u'Google Analytics code',
	            help_text=u'Domain to identify this site through the GA API.'),
	    ]),
	]

From now on, you should be able to set values for your configurations through
the Django admin. And you will, of course, be able to set and retrieve these
values on your code.

	from setmagic import settings

	# Instantly save onto the database!
	settings.FACEBOOK_APP_ID = '000000000000000'

	# Retrieve the setting value from the database
	print(settings.FACEBOOK_APP_ID)

	# Deletes it from the database
	del settings.FACEBOOK_APP_ID

If you added the template context processor like described above, you can also
use SetMagic values on your templates.

	<p>My Facebook app ID is <code>{{ setmagic.FACEBOOK_APP_ID }}</code></p>

See? No mistery. :)


## Platform support

	* Python 2.6+
	* Python 3.x
	* Django 1.5+


## Contribute

You can play with the code at SetMagic's reposity on [GitHub][2] or [donate][3]
me a few bucks from heart so I can write open source code without worrying too
much about bills.


[1]: https://docs.djangoproject.com/en/dev/ref/contrib/admin/
[2]: http://github.com/7ws/django-setmagic
[3]: https://gratipay.com/emyller/
