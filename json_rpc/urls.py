from django.urls import path
from .views import RPCView

urlpatterns = [
    path('', RPCView.as_view(), name='rpc_form'),
]