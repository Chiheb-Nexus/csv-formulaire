from django.urls import path, include, re_path
from form_app import views

urlpatterns = [
    path('', views.Registration.as_view(), name='registration'),
    path('home', views.Home.as_view(), name='home'),
    path('update-db', views.UpdateDB.as_view(), name='updateDB'),
    path('display', views.DisplayPersons.as_view(), name='display'),
    path('stream-csv', views.StreamCSV.as_view(), name='stream_csv')
]