##### MOdel Formset #######

from django.forms import modelformset_factory

from myapp.models import Author

AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))

AuthorFormSet = modelformset_factory(Author, exclude=('birth_date',))
