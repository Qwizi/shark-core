from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import Bonus, Category
from .serializers import CategorySerializer, BonusSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BonusViewSet(viewsets.ModelViewSet):
    serializer_class = BonusSerializer

    def get_queryset(self):
        queryset = Bonus.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = Bonus.objects.filter(category__pk=category)

            if category == '-1':
                queryset = Bonus.objects.all()

        return queryset
