from django.db import models
class Product(models.Model):
    name=models.CharField(max_length=70)
    buy_price=models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    url=models.URLField(max_length=200)
    sell_price=models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    comments=models.TextField()
    source_sell=models.URLField(max_length=200)
    source_buy=models.URLField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    discount_value=models.IntegerField(default=0)
    stock=models.PositiveIntegerField(default=0)
    @property
    def price(self):
        return self.buy_price
    @price.setter
    def price(self, value:int):
        if value==0:
            raise ValueError("Не должно быть 0")
        self.buy_price=value
    @property
    def discount_value(self):
        return self._discount_value
    @discount_value.setter
    def discount_value(self, value: int):
        if not (0<value<=100):
            raise ValueError("Скидка должна быть от 0 до 100%")
        self._discount_value=value
    @property
    def status(self):
        return 'doubtful'
    @property
    def final_price(self):
        final_price=self.price*(1-self._discount_value/100)
        return final_price
    @property
    def profit(self):
        profit=self.sell_price-self.buy_price
        return profit
    @property
    def profit_recent(self):
        profit_recent=(self.profit/self.buy_price)*100
        return profit_recent
    def __str__(self):
        return self.name