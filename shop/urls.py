from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^products/$', views.GetProductListView.as_view(), name='products-view'),
    url(r'^orders/$', views.GetOrderListView.as_view(), name='orders-view'),
    url(r'^create_order/$', views.CreateOrderView.as_view(), name='create-order-view'),
    url(r'^order/change_status/(?P<pk>\w+)/$', views.ChangeStatusFromPaymaster.as_view(), name='change-order-view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
