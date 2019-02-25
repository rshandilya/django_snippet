class FillQuizForm(forms.Form): 
	mark = forms.IntegerField()
    negative_mark = forms.DecimalField(min_value=0, decimal_places=2, max_value=1)

	def __init__(self, *args, **kwargs):
		super(FillQuizForm,self).__init__(*args, **kwargs)
		quiz_option = Quiz.objects.all()
		choice_list = [(q.id, q.title) for q in quiz_option]
		self.fields['quiz'] = forms.ChoiceField(choices=choice_list)


class TestQuestionForm(forms.Form):
	def __init__(self, question, *args, **kwargs):
		super(TestQuestionForm, self).__init__(*args, **kwargs)
		choice_list = question.get_ans_choice()
		self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                           widget=RadioSelect)

class MCQForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(MCQForm, self).__init__(*args, **kwargs)
        choice_list = question.get_ans_choice()
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)
