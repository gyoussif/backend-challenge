import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings')
django.setup()
import random
import datetime
from django.utils import timezone
from django.db import IntegrityError
from apps.review import models

questions_text = [
    'What is your favorite color?',
    'What is your favorite food?',
    'What is your favorite movie?',
    'What is your favorite song?']

choices_text = [
    ['Red', 'Blue', 'Green', 'Yellow'],
    ['Pizza', 'Hamburger', 'Steak', 'Koshary'],
    ['Joker', 'The Godfather', 'The Dark Knight', 'Pulp Fiction'],
    ['Bohemian Rhapsody', 'Ya Ghaly', 'Imagine', 'Unstoppable']
]

def create_questions_and_choices():
    for i in range(len(questions_text)):
        question = models.Question.objects.create(text=questions_text[i])
        for text in choices_text[i]:
            choice=models.Choice.objects.create(text=text)
            question.choices.add(choice)

def create_answers():
    questions = models.Question.objects.all()
    for _ in range(4000):
        question=random.choice(questions)
        review = models.Review.objects.create(submitted_at=random_date())
        choice = random.choice(question.choices.all())
        models.Answer.objects.create(review=review, question=question, choice=choice)

def random_date():
    start = timezone.make_aware(datetime.datetime(2021, 1, 1))
    end = timezone.make_aware(datetime.datetime(2023, 12, 31))
    return timezone.make_aware(datetime.datetime.fromtimestamp(random.randint(start.timestamp(), end.timestamp())))

try:
    create_questions_and_choices()
    create_answers()
except IntegrityError as e:
    print("IntegrityError:", e)