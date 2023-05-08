from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from .models import Subscription
from .serializers import SubscriptionSerializer


# Create your views here.
class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',

        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name', 'user__email'))

    )

    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(self, request, *args, **kwargs)

        response_data = {'result': response.data}

        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data

        return response

    #переопределяем метод