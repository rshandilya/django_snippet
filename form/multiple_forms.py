

#### FOR GET REQUEST ONLY #####
class MainView(TemplateView):
    template_name = 'sample_forms/index.html'

    def get(self, request, *args, **kwargs):
        question_form = QuestionForm(self.request.GET or None)
        answer_form = AnswerForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['answer_form'] = answer_form
        context['question_form'] = question_form
        return self.render_to_response(context)

### TEMPLATE
""" 
<h1>Question Form</h1>
<form action="{% url 'question' %}" method="post">{% csrf_token %}
    {{ question_form }}
    <input type="submit" value="Send Question">
</form>
<h1>Answer Form</h1>
<form action="{% url 'answer' %}" method="post">{% csrf_token %}
    {{ answer_form }}
<input type="submit" value="Send Answer">
</from>
"""


#### FOR POST REQUEST #####

class QuestionFormView(FormView):
    form_class = QuestionForm
    template_name = 'sample_forms/index.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        question_form = self.form_class(request.POST)
        answer_form = AnswerForm()
        if question_form.is_valid():
            question_form.save()
            return self.render_to_response(
                self.get_context_data(
                success=True
            )
        )
        else:
        return self.render_to_response(
        self.get_context_data(
                question_form=question_form,
   
        )


class AnswerFormView(FormView):
    form_class = AnswerForm
    template_name = 'sample_forms/index.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        answer_form = self.form_class(request.POST)
        question_form = QuestionForm()
        if answer_form.is_valid():
            answer_form.save()
            return self.render_to_response(
                self.get_context_data(
                success=True
            )
        )
        else:
            return self.render_to_response(
            self.get_context_data(
                    answer_form=answer_form,
                    question_form=question_form
            )
        )

### TEMPLATE
"""
{% if success %}
   <h1>Your request has been submitted</h1>
{% else %}
  # Forms here
{% endif %}
"""
