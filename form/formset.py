####### Daniel Rubio #####
# forms.py
class DrinkForm(forms.Form):
name = forms.ChoiceField(choices=DRINKS,initial=0)
size = forms.ChoiceField(choices=SIZES,initial=0)
amount = forms.ChoiceField(choices=[(None,'Amount of drinks')]+[(i, i) for i in
range(1,10)])

# views.py
from django.forms import formset_factory

def index(request):
    DrinkFormSet = formset_factory(DrinkForm, extra=2, max_num=20)
    if request.method == 'POST':
        # TODO
    else:
        formset = DrinkFormSet(initial=[{'name': 1,'size': 'm','amount':1}])
    return render(request,'online/index.html',{'formset':formset})

# online/index.html
<form method="post">
{% csrf_token %}
{{ formset.management_form }}
<table>
{% for form in formset %}
<tr><td><ul class="list-inline">{{ form.as_ul }}</ul></td></tr>
{% endfor %}
</table>
<input type="submit" value="Submit order" class="btn btn-primary">
</form>

## FORMSET FACTORY ##
formset_factory(form, formset=BaseFormSet, extra=1, can_order=False, can_delete=False,
                max_num=None, min_num=None, validate_max=False, validate_min=False)

### FORMSET MANAGEMENT FORMS CONTENTS ###
<input type="hidden" name="form-TOTAL_FORMS" value="3" id="id_form-TOTAL_FORMS" />
<input type="hidden" name="form-INITIAL_FORMS" value="1" id="id_form-INITIAL_FORMS" />
<input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS" />
<input type="hidden" name="form-MAX_NUM_FORMS" value="20" id="id_form-MAX_NUM_FORMS" />

#### USING THE FORMSET MANAGER VALUE #####
#views.py
def index(request):
    extra_forms = 2
    DrinkFormSet = formset_factory(DrinkForm, extra=extra_forms, max_num=20)
    if request.method == 'POST':
        if 'additems' in request.POST and request.POST['additems'] == 'true':
            formset_dictionary_copy = request.POST.copy()
            formset_dictionary_copy['form-TOTAL_FORMS'] = int(formset_dictionary_copy['form-TOTAL_FORMS']) + extra_forms
            formset = DrinkFormSet(formset_dictionary_copy)
        else:
            formset = DrinkFormSet(request.POST)
            if formset.is_valid():
                return HttpResponseRedirect('/about/contact/thankyou')
            else:
                formset = DrinkFormSet(initial=[{'name': 1,'size': 'm','amount':1}])
                return render(request,'online/index.html',{'formset':formset})

 # online/index.html
<form method="post">
{% csrf_token %}
{{ formset.management_form }}
<table>
{% for form in formset %}
<tr><td>{{ form }}</td></tr>
{% endfor %}
</table>
<input type="hidden" value="false" name="additems" id="additems">
<button class="btn btn-primary" id="additemsbutton">Add items to order</button>
<input type="submit" value="Submit order" class="btn btn-primary">
</form>
<script>
$(document).ready(function() {
$("#additemsbutton").on('click',function(event) {
$("#additems").val("true");
});
});
</script>


####### CUSTOM FORMSET VALIDATION ########

from django.forms import BaseFormSet
from django.forms import formset_factory
from myapp.forms import ArticleForm

class BaseArticleFormSet(BaseFormSet):
    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        titles = []
        for form in self.forms:
            title = form.cleaned_data['title']
            if title in titles:
                raise forms.ValidationError("Articles in a set must have distinct titles.")
            titles.append(title)

ArticleFormSet = formset_factory(ArticleForm, formset=BaseArticleFormSet)

### ADDING ADDITIONAL FIELDS TO FORM FIELD ###

from django.forms import BaseFormSet
from django.forms import formset_factory
from myapp.forms import ArticleForm

class BaseArticleFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["my_field"] = forms.CharField()
        
ArticleFormSet = formset_factory(ArticleForm, formset=BaseArticleFormSet)
formset = ArticleFormSet()

#### Passing custom parameters to formset forms #####
class MyArticleForm(ArticleForm):
    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

ArticleFormSet = formset_factory(MyArticleForm)
formset = ArticleFormSet(form_kwargs={'user': request.user}) 
### using get_form_kwargs
class BaseArticleFormSet(BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['custom_kwarg'] = index
        return kwargs
   
### formset in template ####
<form method="post">
    {{ formset.management_form }}
    <table>
        {% for form in formset %}
        {{ form }}
        {% endfor %}
    </table>
</form>
###
<form method="post">
    <table>
        {{ formset }}
    </table>
</form>
#####
"""
<form method="post">
    {{ formset.management_form }}
    {% for form in formset %}
        <ul>
            <li>{{ form.title }}</li>
            <li>{{ form.pub_date }}</li>
            {% if formset.can_delete %}
                <li>{{ form.DELETE }}</li>
            {% endif %}
        </ul>
    {% endfor %}
</form>
"""

###### USING MORE THAN ONE FORMS #######

from django.forms import formset_factory
from django.shortcuts import render
from myapp.forms import ArticleForm, BookForm

def manage_articles(request):
    ArticleFormSet = formset_factory(ArticleForm)
    BookFormSet = formset_factory(BookForm)
    if request.method == 'POST':
        article_formset = ArticleFormSet(request.POST, request.FILES, prefix='articles')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if article_formset.is_valid() and book_formset.is_valid():
            # do something with the cleaned_data on the formsets.
            pass
    else:
        article_formset = ArticleFormSet(prefix='articles')
        book_formset = BookFormSet(prefix='books')
    return render(request, 'manage_articles.html', {
        'article_formset': article_formset,
        'book_formset': book_formset,
    })
