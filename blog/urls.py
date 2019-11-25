from django.urls import path
# from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
]
