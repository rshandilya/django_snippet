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

      
###### LISTVIEW ########      
# views.py
from django.views.generic.list import ListView
from .models import Item
class ItemList(ListView):
    model = Item
# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views
urlpatterns = [
    url(r'^$',items_views.ItemList.as_view(),name="index"),
]    

# templates/items/item_list.html
  {% regroup object_list by menu as item_menu_list %}
  {% for menu_section in item_menu_list %}
   <li>{{ menu_section.grouper }}
    <ul>
        {% for item in menu_section.list %}
                <li>{{item.name|title}}</li>   
        {% endfor %}
    </ul>
    </li>
{% endfor %}

####### DETAILVIEW ##########
# views.py
from django.views.generic. import DetailView
from .models import Item
class ItemDetail(DetailView):
    model = Item
# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views
urlpatterns = [
    url(r'^(?P<pk>\d+)/$',items_views.ItemDetail.as_view(),name="detail"),
]
# templates/items/item_detail.html
<h4> {{item.name|title}}</h4>
<p>{{item.description}}</p>
<p>${{item.price}}</p>
<p>For {{item.get_size_display}} size: Only {{item.calories}} calories
{% if item.drink %}
and {{item.drink.caffeine}} mg of caffeine.</p>
{% endif %}
</p>


########  LISTVIEW WITH CUSTOM QUERY  #######
# views.py
from django.views.generic.list import ListView
from .models import Item
class ItemList(ListView):
    model = Item
    queryset = Item.objects.filter(menu__id=1)
    ordering = ['name']


######### LIST OF RECORD WITH PAGINATION  ########
# views.py
from django.views.generic.list import ListView
from .models import Item
class ItemList(ListView):
    model = Item
    paginate_by = 5
# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views
urlpatterns = [
    url(r'^$',items_views.ItemList.as_view(),name="index"),
    url(r'^page/(?P<page>\d+)/$',items_views.ItemList.as_view(),name="page"),
]
# templates/items/item_list.html
  {% regroup object_list by menu as item_menu_list %}
{% for menu_section in item_menu_list %}
   <li>{{ menu_section.grouper }}
    <ul>
        {% for item in menu_section.list %}
        <li>{{item.name|title}}</li>   
        {% endfor %}
    </ul>
    </li>
{% endfor %}
 {% if is_paginated %}
    {{page_obj}}
 {% endif %}

####### DETAILVIEW WITH SLUGFIELD #######
# views.py
from django.views.generic import DetailView
from .models import Item
class ItemDetail(DetailView):
    model = Item
    slug_field = 'name__iexact'
# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views
urlpatterns = [
    url(r'^(?P<slug>\w+)/$',items_views.ItemDetail.as_view(),name="detail"),
]

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
