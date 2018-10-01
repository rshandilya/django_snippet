###### SNIPPET 1 ####### --daniel Rubio

# models.py
class Contact(models.Model):
    name = models.CharField(max_length=50,blank=True)
    email = models.EmailField()
    comment = models.CharField(max_length=1000)

# forms.py
from django import forms
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

# views.py method to process model form
def contact(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = ContactForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/about/contact/thankyou')
        else:
            # GET, generate unbound (blank) form
            form = ContactForm()
            return render(request,'about/contact.html',{'form':form})


###### MODEL FORM FOR RELATED MODELS ########### --Danile Rubio

from django import forms
from django.conf import settings

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None)
    name = models.CharField(max_length=50,blank=True)
    email = models.EmailField()
    comment = models.CharField()

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['user']

def contact(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = ContactForm(request.POST)
        # check if it's valid:
        ########## option 1 ########
        if form.is_valid():
            # Check if user is available
            if request.user.is_authenticated():
                # Add missing user to model form
                form.instance.user = request.user
                # Insert into DB
                form.save()
        ######## option 2 ######
        if form.is_valid():
            # Save instance but don't commit until model instance is complete
            # form.save() returns a materialized model instance that has yet to
            # be saved
            pending_contact = form.save(commit=False)
            # Check if user is available
            if request.user.is_authenticated():
                # Add missing user to model form
                pending_contact.user = request.user
                # Insert into DB
                pending_contact.save()

## SNIPPET 4 ; REF DJANGOGIRLS #######
##### EDITING USING MODEL FORM  ########

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

######### DJANGO DOC  ########

## Save() methods
>>> from myapp.models import Article
>>> from myapp.forms import ArticleForm
>>> f = ArticleForm(request.POST) # Create a form instance from POST data
>>> new_article = f.save()   # Save a new Article object from the form's data.
# Create a form to edit an existing Article, but use
# POST data to populate the form.
>>> a = Article.objects.get(pk=1)
>>> f = ArticleForm(request.POST, instance=a)
>>> f.save()

##### for related model
>>> f = AuthorForm(request.POST)
>>> new_author = f.save(commit=False)
>>> new_author.some_field = 'some_value'
>>> new_author.save() # Save the new instance.   
# Now, save the many-to-many data for the form.
>>> f.save_m2m()



###### Overriding the default fields #######
from django.forms import ModelForm, Textarea
from myapp.models import Author
from django.utils.translation import gettext_lazy as _

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title', 'birth_date')
        widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        labels = {
            'name': _('Writer'),
        }
        help_texts = {
            'name': _('Some useful help text.'),
        }
        error_messages = {
            'name': {
                'max_length': _("This writer's name is too long."),
            },
        }

#### to specify classes ###
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['pub_date', 'headline', 'content', 'reporter', 'slug']
        field_classes = {
            'slug': MySlugFormField,
        }

#### to have comeplte control  ####
class ArticleForm(ModelForm):
    slug = CharField(validators=[validate_slug])

    class Meta:
        model = Article
        fields = ['pub_date', 'headline', 'content', 'reporter', 'slug']

##### Form Inheritance #####
>>> class EnhancedArticleForm(ArticleForm):
...     def clean_pub_date(self):           # extra validation and cleaning for pub_date field
...         ...

>>> class RestrictedArticleForm(EnhancedArticleForm):
...     class Meta(ArticleForm.Meta):       # Inheriting Meta Class
...         exclude = ('body',)

### Providing initial values
>>> article = Article.objects.get(pk=1)
>>> article.headline
'My headline'
>>> form = ArticleForm(initial={'headline': 'Initial headline'}, instance=article)
>>> form['headline'].value()
'Initial headline'      # initial args override the instance value








