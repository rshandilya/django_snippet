####  SNIPPET 1 ####

# forms.py in app named 'contact'
from django import forms
class ContactForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(label='Your email')
    comment = forms.CharField(widget=forms.Textarea)


# views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactForm
def contact(request):
    if request.method == 'POST':
        # POST, generate form with data from the request
        form = ContactForm(request.POST)
        # Reference is now a bound instance with user data sent in POST
        # Call is_valid() to validate data and create cleaned_data and errors
        # dict
        if form.is_valid():
            # Form data is valid, you can now access validated values in the
            # cleaned_data dict
            # e.g. form.cleaned_data['email']
            # process data, insert into DB, generate email
            # Redirect to a new URL
            return HttpResponseRedirect('/about/contact/thankyou')
        
######### PROCESSING BOUND AND UNBOUND GET REQUEST #############
if request.GET.items():
    form = YourForm(request.GET)
    if form.is_valid():
        ...

else:
    form = YourForm()
        else:
            pass # Not needed
        # is_valid() method created errors dict, so form reference now contains
        # errors
        # this form reference drops to the last return statement where errors
        # can then be presented accessing form.errors in a template
    else:
        # GET, generate blank form
        form = ContactForm()
        # Reference is now an unbound (empty) form
        # Reference form instance (bound/unbound) is sent to template for
        # rendering
        return render(request,'about/contact.html',{'form':form})



# template.html
"""
<form method="POST">
{% csrf_token %}
<table>
{{form.as_table}}
</table>
<input type="submit" value="Submit form">
</form>
"""


########## Multiple Submit Button #####
<form action="" method="post">
{{ form_newsletter }}
<input type="submit" name="newsletter_sub" value="Subscribe" />
<input type="submit" name="newsletter_unsub" value="Unsubscribe" />
</form>

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email',)

# in the context of a django.forms form
def clean(self):
    if 'newsletter_sub' in self.data:
        # do subscribe
    elif 'newsletter_unsub' in self.data:
        # do unsubscribe
# another approach
if request.method=='POST' and 'btnform1' in request.POST:
    do something...
if request.method=='POST' and 'btnform2' in request.POST:
    do something...

