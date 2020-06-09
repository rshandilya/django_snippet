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


####  Field value different for creating and editing ####

# Models.py
class Item(models.Model):
    sku = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    added_by = models.ForeignKey(User)
# forms.py
class ItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['sku'].widget.attrs['readonly'] = True
            #self.fields['sku'].disabled = True

    def clean_sku(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sku
        else:
            return self.cleaned_data['sku']
