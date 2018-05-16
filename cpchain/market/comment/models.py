from django.db import models
from django.utils.translation import ugettext_lazy as _


class Comment(models.Model):
    """
    The comment model.
    """
    public_key = models.CharField(_("publicKey"), max_length=200)
    market_hash = models.CharField(_("market hash"), max_length=256,null=False)
    content = models.CharField('comment content', max_length=200)
    rating = models.IntegerField(default=1)
    created = models.DateTimeField('Created', auto_now_add=True)

    def __str__(self):
        return self.public_key


class SummaryComment(models.Model):
    """
    The comment model.
    """
    market_hash = models.CharField("market hash", max_length=256,null=False)
    avg_rating = models.IntegerField("Average rating", default=1)
    sales_number = models.IntegerField("Sales number", default=0)
    updated = models.DateTimeField('Updated', auto_now=True)

    def __str__(self):
        return self.market_hash
