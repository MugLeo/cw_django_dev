from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime

class Question(models.Model):
    created = models.DateField('Creada', auto_now_add=True)
    author = models.ForeignKey(get_user_model(), related_name="questions", verbose_name='Pregunta',
                               on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    user_value = models.PositiveIntegerField("user_value", default=0)
    like = models.BooleanField('Like', default = False)
    dislike = models.BooleanField('Dislike', default = False)

    @property
    def ranking(self):
        ranking = 10 * self.answers.filter(value__gt=0).count()
        ranking = ranking + (5 * self.answers.filter(like=True).count())
        ranking = ranking - (3 * self.answers.filter(dislike=True).count())
        now = datetime.now()
        if self.created == now:
            ranking = ranking +10
        return ranking

    def get_absolute_url(self):
        return reverse('survey:question-edit', args=[self.pk])

class Answer(models.Model):
    ANSWERS_VALUES = ((0,'Sin Responder'),
                      (1,'Muy Bajo'),
                      (2,'Bajo'),
                      (3,'Regular'),
                      (4,'Alto'),
                      (5,'Muy Alto'),)

    question = models.ForeignKey(Question, related_name="answers", verbose_name='Pregunta', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(get_user_model(), related_name="answers", verbose_name='Autor', on_delete=models.CASCADE)
    value = models.PositiveIntegerField("Respuesta", default=0, choices=ANSWERS_VALUES)
    like = models.BooleanField('Like', default = False)
    dislike = models.BooleanField('Dislike', default = False)
    comment = models.TextField("Comentario", default="", blank=True)
