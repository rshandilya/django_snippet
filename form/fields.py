###### FORM FIELDS ########

>>> from django import forms
>>> f = forms.EmailField()
>>> f.clean('foo@example.com')
'foo@example.com'
>>> f.clean('invalid email address')
Traceback (most recent call last):
...
ValidationError: ['Enter a valid email address.']

#### CORE FIELD ARGUMENTS ###########
Field.required
Field.label
Field.label_suffix
Field.initial  Field.help_text, Field.widget, Field.error_messages, Field.validators, 
Field.localize, Field.disabled
Field.has_changed()

