##### MOdel Formset #######

from django.forms import modelformset_factory
from myapp.models import Author

AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))
### model_formset is just extension of formset, can use its parameter.
AuthorFormSet = modelformset_factory(Author, exclude=('birth_date',))

#### CHANGING THE QUERYSET ####
formset =  AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))

## Alternatively
from django.forms import BaseModelFormSet
from myapp.models import Author

class BaseAuthorFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Author.objects.filter(name__startswith='O')

AuthorFormSet = modelformset_factory( Author, 
                                     fields=('name', 'title'), 
                                     formset=BaseAuthorFormSet)

# Formset that doesnt include any pre_exisitng instances.
AuthorFormSet(queryset=Author.objects.none())

## Changing the form¶
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title')

    def clean_name(self):
        # custom validation for the name field

        ...

AuthorFormSet = modelformset_factory(Author, form=AuthorForm)

## Specifying widgets
AuthorFormSet = modelformset_factory(
                Author, fields=('name', 'title'),
                widgets={'name': Textarea(attrs={'cols': 80, 'rows': 20})})

### Enabling localization
AuthorFormSet = modelformset_factory(
...     Author, fields=('name', 'title', 'birth_date'),
...     localized_fields=('birth_date',))


        
