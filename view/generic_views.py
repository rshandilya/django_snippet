from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('about/', TemplateView.as_view(template_name="about.html")),
]


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

#############

# views.py
from django.views.generic import ListView
from books.models import Publisher

class PublisherList(ListView):
    model = Publisher

# urls.py
from django.urls import path
from books.views import PublisherList

urlpatterns = [
    path('publishers/', PublisherList.as_view()),
]
# ..templates/books/publisher_list.html
"""   TEMPLATE
{% extends "base.html" %}

{% block content %}
    <h2>Publishers</h2>
    <ul>
        {% for publisher in object_list %}
            <li>{{ publisher.name }}</li>
        {% endfor %}
    </ul>
{% endblock %}
"""

## Making Friendly Template Context
class PublisherList(ListView):
    model = Publisher
    context_object_name = 'my_favorite_publishers'

## Viewing Subset of Objects / 
class AcmeBookList(ListView):

    context_object_name = 'book_list'
    queryset = Book.objects.filter(publisher__name='ACME Publishing')
    template_name = 'books/acme_list.html'

 ### Dynamic Filtering   
class PublisherBookList(ListView):

    template_name = 'books/books_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)

## modifyinng context data 
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in the publisher
    context['publisher'] = self.publisher
    return context


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
  

#### PERFORMING EXTRA WORK    
class AuthorDetailView(DetailView):

    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj
    

##### RedirectView #######
    
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from articles.models import Article

class ArticleCounterRedirectView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.update_counter()
        return super().get_redirect_url(*args, **kwargs)

#####  REDIRECT FROM URL  ######  
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
# ...
urlpatterns = patterns('',
    # Redirects to the view named app_dashboard (below)
    url(r'^$', RedirectView.as_view(url=reverse_lazy('app_dashboard')), name='index'),
    # Redirects to google.com
    url(r'^$', RedirectView.as_view(url='http://google.com'), name='index'),
    # Our destination URL
    url(r'^dashboard/$', DashboardView.as_view(), name='app_dashboard'),
    # ...
)    
