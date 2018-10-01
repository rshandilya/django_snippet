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

## Model Formset in view ##
from django.forms import modelformset_factory
from django.shortcuts import render
from myapp.models import Author

def manage_authors(request):
    AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))
    if request.method == 'POST':
        formset = AuthorFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = AuthorFormSet()
    return render(request, 'manage_authors.html', {'formset': formset})

### overriding clean
from django.forms import BaseModelFormSet

class MyModelFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        # example custom validation across forms in the formset
        for form in self.forms:
            # your custom formset validation
            ...

## Must modify form.instance
class MyModelFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()

        for form in self.forms:
            name = form.cleaned_data['name'].upper()
            form.cleaned_data['name'] = name
            # update the instance value.
            form.instance.name = name

### Custom Queryset ###
from django.forms import modelformset_factory
from django.shortcuts import render
from myapp.models import Author

def manage_authors(request):
    AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))
    if request.method == "POST":
        formset = AuthorFormSet(
            request.POST, request.FILES,
            queryset=Author.objects.filter(name__startswith='O'),
        )
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        formset = AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))
    return render(request, 'manage_authors.html', {'formset': formset})

## In Templates

<form method="post">
    {{ formset }}
</form>

<form method="post">
    {{ formset.management_form }}
    {% for form in formset %}
        {{ form }}
    {% endfor %}
</form>

<form method="post">
    {{ formset.management_form }}
    {% for form in formset %}
        {% for field in form %}
            {{ field.label_tag }} {{ field }}
        {% endfor %}
    {% endfor %}
</form>

<form method="post">
    {{ formset.management_form }}
    {% for form in formset %}
        {{ form.id }}
        <ul>
            <li>{{ form.name }}</li>
            <li>{{ form.age }}</li>
        </ul>
    {% endfor %}
</form>



