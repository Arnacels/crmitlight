from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .permissions import (ShopStaffPermission, AccountantPermission)
from .models import (Product, Order)
from .serializers import (ProductSerializer, OrderSerializer, CreateOrderSerializer, PartialOrderUpdateSerializer)


class GetProductListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GetOrderView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(~Q(status=0))


class CreateOrderView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.filter()


class GetOrderListView(generics.ListAPIView):
    permission_classes = (AccountantPermission,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(~Q(status=0))
        from_date, to_date = self.request.query_params.get('from_date'), self.request.query_params.get('to_date')
        if self.check_time(from_date):
            from_date = timezone.datetime.fromtimestamp(float(from_date))
            queryset = queryset.filter(date__gte=from_date)
        if self.check_time(to_date):
            to_date = timezone.datetime.fromtimestamp(float(to_date))
            queryset = queryset.filter(date__lte=to_date)
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(id=order_id)
        return queryset

    @staticmethod
    def check_time(date):
        if date:
            if date.isnumeric():
                return True
        return False


class ChangeStatusFromPaymaster(generics.UpdateAPIView):
    permission_classes = (ShopStaffPermission,)
    serializer_class = PartialOrderUpdateSerializer
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        if serializer.instance.status == 3:
            context = {'order': serializer.instance}
            return render(request, 'shop/check.html', context)
        return Response(serializer.data)
