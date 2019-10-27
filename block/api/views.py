from rest_framework import viewsets

from block.models import (
    Block,
    Transaction,
    Vout,
    Vin,
    Address
)
from block.api.serializers import (
    BlockSerializer,
    TransactionSerializer,
    VoutSerializer,
    VinSerializer,
    AddressSerializer,
    OpReturnSerializer,
)
from twitter.models import OpReturn


class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Block.objects.all().order_by('-time')
    serializer_class = BlockSerializer
    filterset_fields = ['hash']
    search_fields = [
        'hash',
        'transaction__vout__asm',
        'transaction__vin__asm',
        'transaction__vout__value',
        'transaction__vout__address__address'
    ]


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all().order_by('-block__time')
    serializer_class = TransactionSerializer
    filterset_fields = ['txid']
    search_fields = [
        'txid',
        'vout__asm',
        'vin__asm',
        'vout__value',
        'vout__address__address'
    ]


class VoutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vout.objects.all().order_by('-tx__block__time')
    serializer_class = VoutSerializer
    filterset_fields = ['asm']
    search_fields = ['asm']


class VinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vin.objects.all().order_by('-tx__block__time')
    serializer_class = VinSerializer
    filterset_fields = ['asm']
    search_fields = ['asm']


class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all().order_by('-vout__tx__block__time')
    serializer_class = AddressSerializer


class OpReturnViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OpReturn.objects.filter(interesting=True)
    serializer_class = OpReturnSerializer