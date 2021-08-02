from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from survey.views import QuestionListView, QuestionCreateView, QuestionUpdateView, answer_question

class TestUrls(SimpleTestCase):

	def test_list_url_resolves(self):
		url = reverse('survey:question-list')
		self.assertEquals(resolve(url).func.view_class, QuestionListView)