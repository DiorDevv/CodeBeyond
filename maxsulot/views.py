from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from maxsulot.models import Product, Comment
from maxsulot.serializers import ProductSerializer, CommentSerializer


class MaxsulotListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()  # author bo‘lmasligi mumkin (agar modelda null=True bo‘lsa)


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Comment.objects.filter(product_id=product_id, parent=None).order_by('-id')

    def perform_create(self, serializer):
        serializer.save()
