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

