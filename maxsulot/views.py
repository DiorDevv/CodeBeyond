from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from maxsulot.models import Product
from maxsulot.serializers import ProductSerializer


class MaxsulotView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Product.objects.all()


class MaxsukotCreateView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(author=user)
        else:
            serializer.save()  # author bo‘lmaydi
