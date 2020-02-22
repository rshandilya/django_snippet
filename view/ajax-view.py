class CreateQuizView(CreateView):
    template_name = "quiz/create_quiz.html"
    form_class = QuizForm
    data = dict()
    #success_url = reverse_lazy("account:profile")

    def render_to_response(self, context, **response_kwargs):
        self.data['quiz_form'] = render_to_string(
            self.get_template_names(),
            context=context,
            request=self.request)
        return JsonResponse(self.data)
        
    def form_valid(self, form):
        #form.instance.owner = self.request.user
        return super(CreateQuizView, self).form_valid(form) 
