from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('<tableName>/',views.showtable,name="showtable"),
]