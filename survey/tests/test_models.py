from django.test import TestCase
from survey.models import Answer, Question
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(username='Leonardo', email="leoanrdo@gmail.com")
        
    def test_is_username(self):
        self.assertEquals(self.user.username,'Leonardo')

    def test_project_total_transactions(self):
        question = Question.objects.create(title="Firs title", description='Firs description', author=self.user)
        self.assertEquals(question.title, 'Firs title')