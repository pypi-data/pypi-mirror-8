django-filtered-mail
====================

Django Email Backend which only sends to whitelisted recipients

This email backend behaves just like the default SMTP backend
except that it only sends messages to a select set of addresses.

Use the setting `EMAIL_ALLOWED_RECIPIENTS` to specify allowed addresses as
regular expressions. The filter uses the Python 'match' method to check
the regular expressions against the email recipients.

It only matches the email addresses and not the optional 'name' part of
recipients. All addresses are lowercased before matching.

Example settings:

    EMAIL_BACKEND = 'django_filtered_mail.mail.EmailBackend'

    EMAIL_ALLOWED_RECIPIENTS = (
        r'^.*@dreamsolution.nl$',
        r'^some.one@gmail.com$',
    )

