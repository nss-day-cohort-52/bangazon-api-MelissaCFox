from django.urls import path
from .views import (CompletedOrders, IncompleteOrders, ExpensiveProducts,
                    InexpensiveProducts)

urlpatterns = [
    path('completedorders', CompletedOrders.as_view()),
    path('incompleteorders', IncompleteOrders.as_view()),
    path('expensiveproducts', ExpensiveProducts.as_view()),
    path('inexpensiveproducts', InexpensiveProducts.as_view())
]
