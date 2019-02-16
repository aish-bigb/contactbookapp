from django.urls import path, include
from . import views
from .views import PhoneBookView

urlpatterns = [
    path('edit/', PhoneBookEdit.as_view(),  name='edit'),
    path('add/', PhoneBookAdd.as_view(),  name='add'),
    path('delete/', PhoneBookAdd.as_view(),  name='delete'),
    path('search/', PhoneBookView.as_view(),  name='search'),
    path('', views.index, name='index'),

]