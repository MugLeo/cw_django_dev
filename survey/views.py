from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from survey.models import Question, Answer
import json

class QuestionListView(ListView):
    model = Question

    def get_context_data(self, **kwargs):
        ctx = super(QuestionListView, self).get_context_data()

        if self.request.user.is_authenticated:
            for i in self.object_list:
                user_value = i.answers.filter(author=self.request.user).first()
                if user_value:
                    i.user_value = user_value.value
                    i.like = user_value.like
                    i.dislike = user_value.dislike
        return ctx

class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description']
    redirect_url = ''

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'


def answer_question(request):
    req = json.loads(request.body)
    question_pk = req['question_pk']
    if not question_pk:
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer = Answer.objects.filter(question=question, author=request.user).first()
    if not answer:
        answer = Answer(question=question)
    old_value = answer.value
    if old_value == req['value']:
        answer.value = 0
    else:
        answer.value = req['value']
    answer.author = request.user
    answer.save()
    return JsonResponse({ 'new_value': answer.value, 'old_value': old_value,'ranking': question.ranking })


def like_dislike_question(request):
    req = json.loads(request.body)
    question_pk = req['question_pk']
    options = req['options']
    if not question_pk:
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer = Answer.objects.filter(question=question, author=request.user).first()
    if not answer:
        answer = Answer(question=question)
    if options == "like":
        if answer.like == True:
            answer.like = False
        else:
            answer.like = True
            answer.dislike = False
    else:
        if answer.dislike == True:
            answer.dislike = False
        else:
            answer.dislike = True
            answer.like = False
    answer.author = request.user
    answer.save()
    return JsonResponse({ 'new_value': answer.like if options == "like" else answer.dislike,
                            'ranking': question.ranking })