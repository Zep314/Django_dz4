from django.urls import path
from .views import index, LastDay


urlpatterns = [
    path('', index, name='index'),
    path('lastday/<int:client_id>/<int:days>', LastDay.as_view(), name='lastday'),
]
