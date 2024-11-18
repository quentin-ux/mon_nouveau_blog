from django.urls import path
from . import views

urlpatterns = [
    path('', views.nauti_list, name='nauti_list'),
    path('equipement/<str:id_equip>/', views.lieu_detail, name='lieu_detail'),
    path('character/<str:id_character>/', views.membre_detail, name='membre_detail'),
    path('character/<str:id_character>/?<str:message>', views.membre_detail, name='membre_detail_mes'),
]