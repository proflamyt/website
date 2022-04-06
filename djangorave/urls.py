# stdlib  imports

# django imports
from django.urls import path, include

# 3rd party imports

# project imports
from djangorave.views import TransactionCreateView


app_name = "djangorave"

urlpatterns = [
    path("transaction/", TransactionCreateView, name="transaction"),
   
]
