from django.urls import path

from maxsulot.views import MaxsulotView, MaxsukotCreateView

urlpatterns = [
    path('posts-list/', MaxsulotView.as_view(), name='maxsulot-list'),
    path('posts-create/', MaxsukotCreateView.as_view(), name='maxsulot-create'),
]