import django
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response

from apps.review import models

from . import serializers
from django.db.models import Count,Q
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.db.models.functions import TruncDate
class ReviewViewSet(GenericViewSet):
    serializer_class = serializers.RetrieveReviewSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        filter_criteria = Q()
        
        if 'from_date' in serializer.validated_data:
            from_date = serializer.validated_data['from_date']
            filter_criteria &= Q(submitted_at__gte=from_date.date())

        if 'to_date' in serializer.validated_data:
            to_date = serializer.validated_data['to_date']
            filter_criteria &= Q(submitted_at__lte=to_date.date())

        reviews = models.Review.objects.filter(filter_criteria).distinct('submitted_at__date')
        results = []
        for review in reviews:
            review_date = review.submitted_at.date()
            answers = models.Answer.objects.filter(review__submitted_at__date=review_date)\
                .select_related('review', 'question', 'choice')
            count=answers.count()
            answers=serializers.AnswerSerializer(answers,many=True)
            results.append({
                'submitted_at': review_date,
                'answers': answers.data,
                'count': count
            })
        return Response(results)
        
    @action(detail=False, methods=['get'])
    def count_per_day(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        filter_criteria = Q()
        
        if 'from_date' in serializer.validated_data:
            from_date = serializer.validated_data['from_date']
            filter_criteria &= Q(review__submitted_at__gte=from_date.date())

        if 'to_date' in serializer.validated_data:
            to_date = serializer.validated_data['to_date']
            filter_criteria &= Q(review__submitted_at__lte=to_date.date())
        
        reviews = models.Answer.objects.filter(filter_criteria).values(
        date=TruncDate('review__submitted_at')
        ).annotate(
            total=Count('id', distinct=True)
        ).order_by('review__submitted_at')
        return Response(reviews)
    
