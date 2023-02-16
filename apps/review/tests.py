from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker
from rest_framework import status
import time
from .models import Answer, Choice, Question, Review


class ReviewAnswersViewTestCase(TestCase):
    def setUp(self):
        self.list_reviews_url = '/api/reviews/'

        self.password = 'password'
        self.admin = User.objects.create_user(
            username='admin', password=self.password, is_superuser=True)
        self.client.login(username=self.admin.username, password=self.password)

        self.review1 = Review.objects.create(
            submitted_at=timezone.now() - timezone.timedelta(days=2))
        self.review2 = Review.objects.create(
            submitted_at=timezone.now() - timezone.timedelta(days=1))
        self.review3 = Review.objects.create(submitted_at=timezone.now())
        self.choice1 = baker.make(Choice)
        self.answer1 = baker.make(Answer, review=self.review1)
        self.answer2 = baker.make(
            Answer, review=self.review2, choice=self.choice1, _quantity=2)
        self.answer3 = baker.make(Answer, review=self.review3, _quantity=3)

    def tearDown(self):
        Review.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Choice.objects.all().delete()

    def test_permissions_no_authentication(self):
        self.client.logout()
        self._test_list_reviews_url(status.HTTP_403_FORBIDDEN)

    def test_permissions_normal_user(self):
        self.user = User.objects.create_user(
            username='user', password=self.password)
        self.client.login(username=self.user.username, password=self.password)
        self._test_list_reviews_url(status.HTTP_403_FORBIDDEN)

    def test_permissions_staff_user(self):
        self.staff = User.objects.create_user(
            username='staff', password=self.password, is_staff=True)
        self.client.login(username=self.staff.username, password=self.password)
        self._test_list_reviews_url(status.HTTP_200_OK,response_size=3)

    def test_list_answers_without_dates(self):
        #test the data returned by the endpoint
        response = self.client.get(self.list_reviews_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        date = self.review1.submitted_at.date()
        self.assertEqual(response.data[0]['count'], 1)
        self.assertEqual(response.data[0]['date'], date)
        self.assertEqual(response.data[0]['answers']
                         [0]['answer'], self.answer1.choice.text)
        self.assertEqual(response.data[0]['answers'][0]['count'], 1)
        self.assertEqual(response.data[1]['answers'][0]['count'], 2)

    def test_list_answers_no_reviews_in_given_period(self):
        data = {
            'from_date': timezone.now() + timezone.timedelta(days=1)
        }
        self._test_list_reviews_url(status.HTTP_404_NOT_FOUND,data=data)

    def test_list_answers_with_from_date(self):
        data = {
            'from_date': timezone.now() - timezone.timedelta(days=1)
        }
        self._test_list_reviews_url(status.HTTP_200_OK,data=data,response_size= 1)

    def test_list_answers_with_to_date(self):
        data = {
            'to_date': timezone.now() - timezone.timedelta(days=1)
        }
        self._test_list_reviews_url(status.HTTP_200_OK,data=data,response_size= 2)

    def test_list_answers_with_from_and_to_dates(self):
        data = {
            'from_date': timezone.now() - timezone.timedelta(days=1),
            'to_date': timezone.now()
        }
        self._test_list_reviews_url(status.HTTP_200_OK,data=data,response_size= 1)

    def test_endpoint_performace(self):
        '''
        Note this test takes long time because of populating the db
        and the time will change depending on the device running the test
        Response time for 4000 reviews: 0.05 seconds
        Response time for 8000 reviews: 0.06 seconds
        Response time for 12000 reviews: 0.08 seconds
        Response time for 16000 reviews: 0.09 seconds
        Response time for 20000 reviews: 0.12 seconds
        '''
        for i in range(1,6):
            baker.make(Answer,_quantity=4000)
            start_time = time.time()
            response = self.client.get(self.list_reviews_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            end_time = time.time()
            response_time = end_time - start_time
            print(f'Response time for {i*4000} reviews: {response_time:.2f} seconds')

    def _test_list_reviews_url(self, status,data=None,response_size=None):
        response = self.client.get(self.list_reviews_url, data)
        self.assertEqual(response.status_code, status)
        if response_size:
            self.assertEqual(len(response.data), response_size)