### CRUD Opeeration using class based views

## CREATE
# views.py
from django.views.generic.edit import CreateView
from .models import Item, ItemForm
from django.core.urlresolvers import reverse_lazy

class ItemCreation(CreateView):
	model = Item
	form_class = ItemForm
	success_url = reverse_lazy('items:index')

# models.py
from django import forms
from django.db import models

class Menu(models.Model):
	name = models.CharField(max_length=30)

class Item(models.Model):
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=100)

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = '__all__'
		widgets = {
		'description': forms.Textarea(),
		}


# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views

urlpatterns = [
url(r'^new/$', items_views.ItemCreation.as_view(), name='new'),
]

# templates/items/item_form.html
"""
<form method="post">
{% csrf_token %}
{{ form.as_p }}
<button type="submit" class="btn btn-primary">Create</button>
</form>
"""
# Option 2
# views.py
from django.views.generic.edit import CreateView
from .models import Item, ItemForm, Menu

class ItemCreation(CreateView):
	template_name = "items/item_form.html" # If not default <app_name>/<model_name>_form.html
	context_type = "text/html" # Default MIME is "text/html"
	model = Item
	form_class = ItemForm
	success_url = reverse_lazy('items:index')

	def get_context_data(self,**kwargs): 
		kwargs['special_context_variable'] = 'My special context variable!!!'
		context = super(ItemCreation, self).get_context_data(**kwargs)
		return context

## Option 3
# views.py

class ItemCreation(CreateView):
	initial = {'size':'L'}
	model = Item
	form_class = ItemForm
	success_url = reverse_lazy('items:index')

	def get_initial(self):
		initial_base = super(ItemCreation, self).get_initial()
		initial_base['menu'] = Menu.objects.get(id=1)
		return initial_base  # must return dictionary

## Option 4
# views.py
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

## Option 5
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
		# get_success_url() is used to get success_url field value
	
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


########## Reading Records ################
## Simple ListView
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
# convention template path: <app_name>/<model_name>_list.html
# context variable name is object_list
"""
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
"""
# Option 2
# views.py
from django.views.generic.list import ListView
from .models import Item

class ItemList(ListView):
	model = Item
	queryset = Item.objects.filter(menu__id=1)
	ordering = ['name']


# ListView 3
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
"""
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
"""

## Simple DetailView
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
"""
<h4> {{item.name|title}}</h4>
<p>{{item.description}}</p>
<p>${{item.price}}</p>
<p>For {{item.get_size_display}} size: Only {{item.calories}} calories
{% if item.drink %}
and {{item.drink.caffeine}} mg of caffeine.</p>
{% endif %}
</p>
"""
## DetailView 2
# views.py
from django.views.generic import DetailView
from .models import Item

class ItemDetail(DetailView):
	model = Item
	slug_field = 'name__iexact' # iexact for case insensitive search

# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views

urlpatterns = [
	url(r'^(?P<slug>\w+)/$',items_views.ItemDetail.as_view(),name="detail"),
]


### UpdateView 2
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
# context variable name is object
# default template : <app_name>/<model_name>_form.html 
"""
<form method="post">
{% csrf_token %}
{{ form.as_p }}
<button type="submit" class="btn btn-primary">
{% if object == None%}Create{% else %}Update{% endif %}
</button>
</form>
"""
### DeleteView
# views.py
from django.views.generic.edit import DeleteView
from .models import Item

class ItemDelete(DeleteView):
	model = Item
	success_url = reverse_lazy('items:index')

# urls.py
from django.conf.urls import url
from coffeehouse.items import views as items_views

urlpatterns = [
	url(r'^delete/(?P<pk>\d+)/$', items_views.ItemDelete.as_view(), name='delete'),
]

# templates/items/item_confirm_delete.html
# Convention Template Location:  <app_name>/<model_name>_confirm_delete.html
# Context Variable: object
<form method="post">
{% csrf_token %}
Do you really want to delete "{{ object }}"?
<button class="btn btn-primary" type="submit">Yes, remove it!</button>
</form>
