##### TemplateViews
# views.py
from django.views.generic import TemplateView
class AboutIndex(TemplateView):
      template_name = 'index.html'
     
      def get_context_data(self, **kwargs):
         # **kwargs contains keyword context initialization values (if any)
         # Call base implementation to get a context
         context = super(AboutIndex, self).get_context_data(**kwargs)
         # Add context data to pass to template
         context['aboutdata'] = 'Custom data'
         return context
         
#urls.py
from coffeehouse.about.views import AboutIndex
urlpatterns = [
    url(r'^about/index/',AboutIndex.as_view(),{'onsale':True}),
]

############# SNIPPET 2  ##########
# views.py
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render

class ContactPage(View):
    mytemplate = 'contact.html'
    unsupported = 'Unsupported operation'
    def get(self, request):
        return render(request, self.mytemplate)
    def post(self, request):
        return HttpResponse(self.unsupported)

#urls.py
from coffeehouse.contact.views import ContactPage
urlpatterns = [
    url(r'^contact/$',ContactPage.as_view()),
]

############# SNIPPET 3  ##########
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

    
    
  
