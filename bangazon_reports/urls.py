from django.urls import path
from .views import (CompletedOrders, IncompleteOrders)

urlpatterns = [
    path('/completedorders', CompletedOrders.as_view()),
    path('/incompleteorders', IncompleteOrders.as_view())
]
