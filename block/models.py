import subprocess

from django.db import (
    models,
    transaction,
    utils
)

from block.utils import (
    get_block,
    get_block_hash,
    get_transaction
)


class Block(models.Model):
    hash = models.CharField(max_length=1255, unique=True)
    confirmations = models.BigIntegerField()
    size = models.IntegerField()
    height = models.IntegerField()
    version = models.IntegerField()
    pow_algo_id = models.IntegerField()
    pow_algo = models.CharField(max_length=1255)
    pow_hash = models.CharField(max_length=1255)
    merkleroot = models.CharField(max_length=1255)
    time = models.BigIntegerField()
    nonce = models.BigIntegerField()
    bits = models.CharField(max_length=1255)
    difficulty = models.FloatField()
    chainwork = models.CharField(max_length=1255)
    previousblockhash = models.CharField(max_length=1255)
    nextblockhash = models.CharField(max_length=1255)

    def __name__(self):
        return self.hash

    @classmethod
    @transaction.atomic
    def new(cls, block_hash=None, block_id=None):
        if block_hash is None and block_id is None:
            return

        if block_hash is None:
            try:
                block_hash = get_block_hash(block_id)
            except subprocess.CalledProcessError as e:
                print(e)
                return

        data = get_block(block_hash)
        txs = data['tx']
        del data['tx']
        try:
            b = cls.objects.create(**data)
        except utils.IntegrityError as e:
            print(e)
            return

        for tx in txs:
            Transaction.new(tx, b)


class Transaction(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    txid = models.CharField(max_length=1255)
    version = models.IntegerField()
    locktime = models.IntegerField()

    @classmethod
    @transaction.atomic
    def new(cls, txid, b):
        try:
            d = get_transaction(txid)
        except subprocess.CalledProcessError as e:
            print(e)
            return
        tx = cls.objects.create(
            block=b,
            txid=d['txid'],
            version=d['version'],
            locktime=d['locktime'],
        )
        for vin in d['vin']:
            Vin.new(vin, tx)

        for vout in d['vout']:
            Vout.new(vout, tx)


class Vin(models.Model):
    tx = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    vout = models.IntegerField(null=True, default=None, blank=True)
    asm = models.CharField(max_length=1255, null=True, default=None, blank=True)
    hex = models.CharField(max_length=1255, null=True, default=None, blank=True)
    sequence = models.BigIntegerField(blank=True, null=True, default=None)
    coinbase = models.CharField(max_length=1255, null=True, default=None, blank=True)
    scriptsig = models.BooleanField(default=False)
    scriptpubkey = models.BooleanField(default=False)

    @classmethod
    @transaction.atomic
    def new(cls, vin, tx):
        data = vin
        if 'scriptPubKey' in data:
            data.update(data['scriptPubKey'])
            data['scriptpubkey'] = True
            del data['scriptPubKey']
        elif 'scriptSig' in data:
            data.update(data['scriptSig'])
            data['scriptsig'] = True
            del data['scriptSig']

        if 'txid' in data:
            del data['txid']

        cls.objects.create(
            tx=tx,
            **data
        )


class Vout(models.Model):
    tx = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    value = models.FloatField()
    n = models.IntegerField()
    asm = models.CharField(max_length=1255, null=True, default=None, blank=True)
    hex = models.CharField(max_length=1255, null=True, default=None, blank=True)
    reqSigs = models.IntegerField(null=True, default=None, blank=True)
    type = models.CharField(max_length=1255, null=True, default=None, blank=True)

    @classmethod
    @transaction.atomic
    def new(cls, vin, tx):
        addr = []
        data = vin
        if 'scriptPubKey' in data:
            if 'addresses' in data['scriptPubKey']:
                addr = data['scriptPubKey']['addresses']
                del data['scriptPubKey']['addresses']
            data.update(data['scriptPubKey'])
            del data['scriptPubKey']

        vout = cls.objects.create(
            tx=tx,
            **data
        )

        for a in addr:
            Address.objects.create(
                vout=vout,
                address=a
            )


class Address(models.Model):
    vout = models.ForeignKey(Vout, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)