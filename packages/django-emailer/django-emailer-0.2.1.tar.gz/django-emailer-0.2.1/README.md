# django-emailer

Template based email sending with SMTP connection management. Use this along
with your transactional email sending provider.


## Install

Get ready for a long process.

	$ pip install django-emailer

Add `'emailer'` to your `INSTALLED_APPS` setting then migrate/sync
emailer models into the database.

	$ python manage.py syncdb

Done.


## How to use

You now have two new entities to play with: `ConnectionProfile` and
`EmailTemplate`. Reach them through Django's admin to configure new SMTP
connections to use and set up your email templates as such:

* `Name`: uppercase, underscode-separated words, **invariable** name to
define your template.
* `Connection profile`: the STMP connection profile you created.
* `Base template name`: set a different one of yours if you need a fancy
email template. Otherwise, `email/default.html` is just fine.
* `Subject`: your email subject. Accepts Django context dictionary.
* `Content`: you email body. Will be rendered into the `{{ content }}`
template variable. Accepts Django context dictionary, of course.

emailer has a very simple API, usable as follows:

	from emailer.models import EmailTemplate


	email = EmailTemplate.get('YOUR_EMAIL_TEMPLATE_NAME').render(
		to='recipient@example.com',
		context={
			'customer_name': 'John Doe',
		})
	email.send()

Note that the `context` argument will be used for both the subject and
content of your email.

**Protip**: Load your email templates into a fixture to ease the deploy
process. You may also need to have them dumped into test fixtures if you
[hopefully] write unit tests to your application.
