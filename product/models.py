from django.db import models
class Product(models.Model):
    STATUS=[("profitable", "выгодный"), ("doubtful", "сомнительно"), ("unprofitable", "невыгодно")]
    name=models.CharField(max_length=70)
    status=models.CharField(max_length=15, choices=STATUS, default="doubtful")
    buy_price=models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    url=models.URLField(max_length=200)
    sell_price=models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    comments=models.TextField()
    source_sell=models.URLField(max_length=200)
    source_buy=models.URLField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    def profit(self):
        profit=self.sell_price-self.buy_price
        return profit
    def profit_recent(self):
        profit_recent=(self.profit()/self.buy_price)*100
        return profit_recent
    def __str__(self):
        return self.name