from datetime import datetime

from django.db import models, transaction
import tqdm

from block.models import Vout


class OpReturn(models.Model):
    interesting = models.BooleanField(default=False)
    message = models.CharField(
        max_length=1255,
        null=True,
        blank=True,
        default=None
    )
    vout = models.ForeignKey(Vout, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)

    order_by = "vout__tx__block__time"

    @classmethod
    @transaction.atomic
    def update(cls):
        candidates = Vout.objects.filter(
            asm__contains="OP_RETURN",
            address=None,
            value=0.0,
            type="nulldata",
            opreturn=None
        )
        for c in tqdm.tqdm(candidates):
            message = None
            try:
                message = str(bytearray.fromhex(c.hex).decode())[2:]
            except UnicodeDecodeError:
                pass
            cls.objects.create(
                interesting=message is not None,
                vout=c,
                message=message
            )

    def format(self):
        dt = datetime.fromtimestamp(self.vout.tx.block.time)
        dt = dt.strftime("%Y/%m/%d, %H:%M:%S")
        return "{} \n {} \n {}".format(self.message, dt, self.vout.tx.txid)
