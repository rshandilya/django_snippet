from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('about/', TemplateView.as_view(template_name="about.html")),
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
    
    
