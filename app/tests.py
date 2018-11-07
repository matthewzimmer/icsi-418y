from django.test import TestCase
from django.utils import timezone
from app.models import Question

# Create your tests here.
class QuestionTestCase(TestCase):
    def setUp(self):
        Question.objects.create(question_text="How", pub_date=timezone.now())

    def test_questions_can_be_asked(self):
        question = Question.objects.get(question_text="How")
        assert hasattr(question, "question_text")