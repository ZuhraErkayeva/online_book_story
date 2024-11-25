from django.urls import path
from .views import book_list,order_create,author_detail
urlpatterns = [
    path('',book_list,name='book_list'),
    path('order_create/',order_create,name='order_create'),
    path('author_detail/',author_detail,name='author_detail'),
]