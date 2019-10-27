from rest_framework import serializers

from block.models import (
    Block,
    Transaction,
    Vout,
    Vin,
    Address
)
from twitter.models import OpReturn


class BlockSerializer(serializers.ModelSerializer):
    tsx = serializers.SerializerMethodField()

    class Meta:
        model = Block
        fields = '__all__'

    def get_tsx(self, obj):
        return TransactionSerializer(
            obj.transaction_set.all(),
            many=True,
        ).data


class TransactionSerializer(serializers.ModelSerializer):
    vout = serializers.SerializerMethodField()
    vin = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_vout(self, obj):
        return VoutSerializer(
            obj.vout_set.all(),
            many=True,
        ).data

    def get_vin(self, obj):
        return VinSerializer(
            obj.vin_set.all(),
            many=True,
        ).data


class VoutSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        return AddressSerializer(
            obj.address_set.all(),
            many=True,
        ).data

    class Meta:
        model = Vout
        fields = '__all__'


class VinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vin
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OpReturnSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OpReturn
        fields = '__all__'