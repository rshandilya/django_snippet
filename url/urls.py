#### simple urls configuration ######

from django.urls import path

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]

# USING REGULAR EXPRESSION
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
]

# USING NESTED ARGUMENTS
from django.urls import re_path

urlpatterns = [
    re_path(r'^blog/(page-(\d+)/)?$', blog_articles),                  # bad
    re_path(r'^comments/(?:page-(?P<page_number>\d+)/)?$', comments),  # good
]

# INCLUDING OTHER URL

from django.urls import include, path
from apps.main import views as main_views
from credit import views as credit_views

extra_patterns = [
    path('reports/', credit_views.report),
    path('reports/<int:id>/', credit_views.report),
    path('charge/', credit_views.charge),
]

urlpatterns = [
    path('', main_views.homepage),
    path('help/', include('apps.help.urls')),
    path('credit/', include(extra_patterns)),
]

# STATING COMMON PATH ONLY ONCE 
from django.urls import include, path
from . import views

urlpatterns = [
    path('<page_slug>-<page_id>/', include([
        path('history/', views.history),
        path('edit/', views.edit),
        path('discuss/', views.discuss),
        path('permissions/', views.permissions),
    ])),
]

##### CAPTURED PARAMETER #########
# In settings/urls/main.py
from django.urls import include, path

urlpatterns = [
    path('<username>/blog/', include('foo.urls.blog')),
]

# In foo/urls/blog.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog.index),
    path('archive/', views.blog.archive),
]

###### PASSING EXTRA OPTION TO 
from django.urls import path
from . import views

urlpatterns = [
    path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
]

## PASSING EXTRA OPTION TO INCLUDE  ####
# main.py
from django.urls import include, path

urlpatterns = [
    path('blog/', include('inner'), {'blog_id': 3}),
]

# inner.py
from django.urls import path
from mysite import views

urlpatterns = [
    path('archive/', views.archive),
    path('about/', views.about),
]

#### SET 2 #####
# main.py
from django.urls import include, path
from mysite import views

urlpatterns = [
    path('blog/', include('inner')),
]

# inner.py
from django.urls import path

urlpatterns = [
    path('archive/', views.archive, {'blog_id': 3}),
    path('about/', views.about, {'blog_id': 3}),
]


####### reverse ######
from news import views

path('archive/', views.archive, name='news-archive')

# using the named URL
reverse('news-archive')

# passing a callable object
# (This is discouraged because you can't reverse namespaced views this way.)
from news import views
reverse(views.archive)

from django.urls import reverse

def myview(request):
    return HttpResponseRedirect(reverse('arch-summary', args=[1945]))

reverse('admin:app_list', kwargs={'app_label': 'auth'}) 


############### JSON RESPONSE ##########################

from django.http import JsonResponse

def send_json(request):

    data = [{'name': 'Peter', 'email': 'peter@example.org'},
            {'name': 'Julia', 'email': 'julia@example.org'}]

    return JsonResponse(data, safe=False)
