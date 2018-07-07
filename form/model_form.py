###### SNIPPET 1 #######

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



from django import forms
from django.conf import settings
class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None)
    name = models.CharField(max_length=50,blank=True)
    email = models.EmailField()
    comment = models.CharField()

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
