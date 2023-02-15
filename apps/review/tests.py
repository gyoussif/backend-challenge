from django.test import TestCase
from django.utils import timezone
from .models import Review, Question, Choice, Answer
from django.contrib.auth.models import User
from model_bakery import baker

class ReviewAnswersViewTestCase(TestCase):
    def setUp(self):
        self.list_reviews_url='/api/reviews/'
        self.count_reviews_per_day_url='/api/reviews/count_per_day/'

        self.password='password'
        self.admin = User.objects.create_user(username='admin', password=self.password,is_superuser=True)
        self.client.login(username=self.admin.username, password=self.password)

        self.review1 = Review.objects.create(submitted_at=timezone.now() - timezone.timedelta(days=2))
        self.review2 = Review.objects.create(submitted_at=timezone.now() - timezone.timedelta(days=1))
        self.review3 = Review.objects.create(submitted_at=timezone.now())
        
        baker.make(Answer,review=self.review1)
        baker.make(Answer,review=self.review2)
        baker.make(Answer,review=self.review3)
    
    def tearDown(self):
        Review.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Review.objects.all().delete()

    def test_permissions_no_authentication(self):
        self.client.logout()
        self._test_permission(403)
    
    def test_permissions_normal_user(self):
        self.user = User.objects.create_user(username='user', password=self.password)
        self.client.login(username=self.user.username, password=self.password)
        self._test_permission(403)
    
    def test_permissions_staff_user(self):
        self.staff = User.objects.create_user(username='staff', password=self.password,is_staff=True)
        self.client.login(username=self.staff.username, password=self.password)
        self._test_permission(200)

    def _test_permission(self, status):
        response = self.client.get(self.list_reviews_url)
        self.assertEqual(response.status_code, status)
        response = self.client.get(self.list_reviews_url)
        self.assertEqual(response.status_code, status)


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
