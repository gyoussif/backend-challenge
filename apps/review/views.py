import pandas as pd
from django.db.models import F, Q
from django.db.models.functions import TruncDate
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status


from apps.review import models

from . import permissions, serializers


class ReviewViewSet(GenericViewSet):
    serializer_class = serializers.RetrieveReviewSerializer
    permission_classes = [permissions.IsAdminOrStaffUser]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        filter_criteria = Q()

        if 'from_date' in serializer.validated_data:
            from_date = serializer.validated_data['from_date']
            filter_criteria &= Q(review__submitted_at__gte=from_date)

        if 'to_date' in serializer.validated_data:
            to_date = serializer.validated_data['to_date']
            filter_criteria &= Q(review__submitted_at__lte=to_date)

        answers = models.Answer.objects.filter(filter_criteria).values(
            answer=F('choice__text'),
            date=TruncDate('review__submitted_at')
        )
        if not answers:
            return Response(status=status.HTTP_404_NOT_FOUND)
        df = pd.DataFrame(answers)
       # Group by date and answer, count occurrences of each group
        counts = df.groupby(
            ['date', 'answer']).size().reset_index(name='count')
        # Group by date, create a nested dictionary
        result = []
        for date, group in counts.groupby('date'):
            group.pop('date')
            answers = group.to_dict('records')
            result.append(
                {'date': date, 'answers': answers, 'count': group['count'].sum()})
        return Response(result, status=status.HTTP_200_OK)
