############ FormView #############
# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
#vies.py
from myapp.forms import ContactForm
from django.views.generic.edit import FormView

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


############# ModelForm ##############
from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

# views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from myapp.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

# CreateView and UpdateView use myapp/author_form.html
# DeleteView uses myapp/author_confirm_delete.html

####### FOREIGNKEY #######
from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # ...

# Views.py    
from django.views.generic.edit import CreateView
from myapp.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)    


############# SNIPPET   ##########
# views.py
from django.views.generic.edit import CreateView
from .models import Item, ItemForm, Menu
class ItemCreation(CreateView):
    template_name = "items/item_form.html"
    context_type = "text/html"
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('items:index')
    def get_context_data(self,**kwargs):
        kwargs['special_context_variable'] = 'My special context variable!!!'
        context = super(ItemCreation, self).get_context_data(**kwargs)
        return context        

############# SNIPPET 4  ##########
# views.py
from django.views.generic.edit import CreateView
from .models import Item, ItemForm, Menu
class ItemCreation(CreateView):
    initial = {'size':'L'}
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('items:index')
    def get_initial(self):
        initial_base = super(ItemCreation, self).get_initial()
        initial_base['menu'] = Menu.objects.get(id=1)
        return initial_base

      
# views.py
from django.views.generic.edit import CreateView
from .models import Item, ItemForm, Menu
class ItemCreation(CreateView):
    initial = {'size':'L'}
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('items:index')
    def get_form(self):
        form = super(ItemCreation, self).get_form()
        initial_base = self.get_initial()
        initial_base['menu'] = Menu.objects.get(id=1)
        form.initial = initial_base
        form.fields['name'].widget = forms.widgets.Textarea()
        return form


# views.py
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Item, ItemForm, Menu
class ItemCreation(CreateView):
    initial = {'size':'L'}
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('items:index')
    def form_valid(self,form):
        super(ItemCreation,self).form_valid(form)
        # Add action to valid form phase
        messages.success(self.request, 'Item created successfully!')
        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self,form):
        # Add action to invalid form phase
        return self.render_to_response(self.get_context_data(form=form))


###### TO ADD FOREIGNKEY IN CREATEVIEW #######
class CreateArticle(CreateView):
    model = Article

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        #article.save()  # This is redundant, see comments.
        return super(CreateArticle, self).form_valid(form)
## method 2
class CreateArticle(CreateView):
    model = Article

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateArticle, self).form_valid(form)

###################
# views.py
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.contrib import messages

class ItemCreation(CreateView):
    initial = {'size':'L'}
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('items:index')
    template_name = "items/item_form.html"
    
    def get(self,request, *args, **kwargs):
        form = super(ItemCreation, self).get_form()
        # Set initial values and custom widget
        initial_base = self.get_initial()
        initial_base['menu'] = Menu.objects.get(id=1)
        form.initial = initial_base
        form.fields['name'].widget = forms.widgets.Textarea()
        # return response using standard render() method
        return render(request,self.template_name,
                      {'form':form,
                       'special_context_variable':'My special context variable!!!'})
    
    def post(self,request,*args, **kwargs):
        form = self.get_form()
        # Verify form is valid
        if form.is_valid():
            # Call parent form_valid to create model record object
            super(ItemCreation,self).form_valid(form)
            # Add custom success message
            messages.success(request, 'Item created successfully!')   
            # Redirect to success page   
            return HttpResponseRedirect(self.get_success_url())
        # Form is invalid
        # Set object to None, since class-based view expects model record object
        self.object = None
        # Return class-based view form_invalid to generate form with errors
        return self.form_invalid(form)

      




########## UPDATE VIEW ############
# views.py
from django.views.generic import UpdateView
from .models import Item
class ItemUpdate(UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('items:index')
# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views
urlpatterns = [
     url(r'^edit/(?P<pk>\d+)/$', items_views.ItemUpdate.as_view(), name='edit'),
]
# templates/items/item_form.html
<form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">
          {% if object == None%}Create{% else %}Update{% endif %}
        </button>
</form>

##########  DELETE VIEW ############
# views.py
from django.views.generic.edit import DeleteView
from .models import Item
class ItemDelete(UpdateView):
    model = Item
    success_url = reverse_lazy('items:index')
# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views
urlpatterns = [
    url(r'^delete/(?P<pk>\d+)/$', items_views.ItemDelete.as_view(), name='delete'), 
]
# templates/items/item_confirm_delete.html
  <form method="post">
        {% csrf_token %}
        Do you really want to delete "{{ object }}"?
        <button class="btn btn-primary" type="submit">Yes, remove it!</button>
  </form>

####### DELETE VIEW FOR MULTIPLE PARAMETER ########
class ReportScheduleDeleteView(DeleteView):
    model = ReportSchedule
    template_name = "report/report_confirm_delete.html"
    success_url = lazy(reverse, str)('jsclient-list')

    # Get the parameters passed in the url so they can be used in the 
    # "report/report_confirm_delete.html"     

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        client = self.kwargs['pk']
        report = self.kwargs['rpk']

        queryset = ReportSchedule.objects.filter(client_id=client, id=report)

        if not queryset:
            raise Http404

        context = {'client_id':client, 'report_id':report}
        return context

    # Override the delete function to delete report Y from client X
    # Finally redirect back to the client X page with the list of reports
    def delete(self, request, *args, **kwargs):
        client = self.kwargs['pk']
        report = self.kwargs['rpk']

        clientReport = ReportSchedule.objects.filter(client_id=client, id=report)
        clientReport.delete()

        return HttpResponseRedirect(reverse('report-list', kwargs={'pk': client})


####### CLASS BASED WITH MIXIN ##########
# views.py
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Item, ItemForm
class ItemCreation(SuccessMessageMixin,CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('items:index')
    success_message = "Item %(name)s created successfully"

################# AJAX #################
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from myapp.models import Author

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class AuthorCreate(AjaxableResponseMixin, CreateView):
    model = Author
    fields = ['name']
                                    
                                    
                                    
