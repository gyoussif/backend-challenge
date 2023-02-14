from django.test import TestCase
from django.utils import timezone
from .models import Review, Question, Choice, Answer

class ReviewAnswersViewTestCase(TestCase):
    def setUp(self):
        self.list_reviews_url='/api/reviews/'
        self.count_reviews_per_day_url='/api/reviews/count_per_day/'
        self.question1 = Question.objects.create(text='Question 1')
        self.question2 = Question.objects.create(text='Question 2')
        self.choice1 = Choice.objects.create(text='Choice 1')
        self.choice2 = Choice.objects.create(text='Choice 2')
        self.question1.choices.add(self.choice1, self.choice2)
        self.question2.choices.add(self.choice1, self.choice2)

        self.review1 = Review.objects.create(submitted_at=timezone.now() - timezone.timedelta(days=2))
        self.review2 = Review.objects.create(submitted_at=timezone.now() - timezone.timedelta(days=1))
        self.review3 = Review.objects.create(submitted_at=timezone.now())

        self.answer1 = Answer.objects.create(review=self.review1, question=self.question1, choice=self.choice1)
        self.answer2 = Answer.objects.create(review=self.review1, question=self.question2, choice=self.choice2)
        self.answer3 = Answer.objects.create(review=self.review2, question=self.question1, choice=self.choice2)
        self.answer4 = Answer.objects.create(review=self.review2, question=self.question2, choice=self.choice1)
        self.answer5 = Answer.objects.create(review=self.review3, question=self.question1, choice=self.choice1)
        self.answer6 = Answer.objects.create(review=self.review3, question=self.question2, choice=self.choice2)

    def test_list_answers_without_dates(self):
        response = self.client.get(self.list_reviews_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_list_answers_with_from_date(self):
        data={
            'from_date':timezone.now() - timezone.timedelta(days=1)
        }
        response = self.client.get(self.list_reviews_url,data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_answers_with_to_date(self):
        data={
            'to_date':timezone.now() - timezone.timedelta(days=1)
        }
        response = self.client.get(self.list_reviews_url,data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_answers_with_from_and_to_dates(self):
        data={
            'from_date':timezone.now() - timezone.timedelta(days=1),
            'to_date':timezone.now()
        }
        response = self.client.get(self.list_reviews_url,data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_count_reviews_per_day_without_dates(self):
        response = self.client.get(self.count_reviews_per_day_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
