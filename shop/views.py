import datetime
from rest_framework import generics, permissions
from .permissions import (PaymasterPermission, ShopAssistantPermission, AccountantPermission)
from .models import (Product, Order)
from .serializers import (ProductSerializer, OrderSerializer, CreateOrderSerializer, PartialUpdateSerializer)


class GetProductListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GetOrderListView(generics.ListAPIView):
    permission_classes = (AccountantPermission,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        from_date, to_date = self.request.query_params.get('from_date'), self.request.query_params.get('to_date')
        if all((from_date, to_date, from_date.isnumeric(), to_date.isnumeric(),)):
            from_date = datetime.date.fromtimestamp(float(from_date))
            to_date = datetime.date.fromtimestamp(float(to_date))
            return self.queryset.filter(date_gte=from_date, date_lte=to_date)


class CreateOrderView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()


class ChangeStatusFromPaymaster(generics.UpdateAPIView):
    permission_classes = (PaymasterPermission, )
    serializer_class = PartialUpdateSerializer
    queryset = Order.objects.all()
