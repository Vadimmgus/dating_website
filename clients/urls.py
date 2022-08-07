from django.urls import path

from clients import views

app_name = 'clients'

urlpatterns = [
    path('list/', views.UserViewSet.as_view({'get': 'list'}), name='list'),
    path('clients/create/', views.UserViewSet.as_view({'post': 'create'}), name='create_client'),
    path('clients/<int:pk>/match/', views.UserMatchViewSet.as_view({'post': 'like'}), name='like'),
]
