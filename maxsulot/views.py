from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

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


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSuperUser]

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.serializer_class(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Product successfully updated",
                "data": serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Product successfully deleted",
            }
        )


class CommentListApiViews(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['id']
        # Berilgan productga tegishli commentlarni olib keladi
        return Comment.objects.filter(product_id=product_id, parent__isnull=True)  # faqat asosiy commentlar


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs['id']
        product = Product.objects.get(id=product_id)
        serializer.save(author=self.request.user, product=product)
