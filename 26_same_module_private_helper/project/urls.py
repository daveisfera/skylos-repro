from django.urls import path
from checkout.views import OrderView

urlpatterns = [path("order/", OrderView.as_view())]
