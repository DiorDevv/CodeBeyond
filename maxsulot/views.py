from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

from maxsulot.models import Product, Comment
from maxsulot.permessions import IsSuperUser
from maxsulot.serializers import ProductSerializer, CommentSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Product.objects.all()


class ProductCreateView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
