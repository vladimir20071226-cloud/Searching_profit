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
    discount_value=models.IntegerField(default=0)
    @property
    def price(self):
        return self.buy_price
    @price.setter
    def price(self, value:int):
        if value<0:
            raise ValueError("Не должно быть отрицательным")
        self.buy_price=value
    @property
    def discount(self):
        return self.discount_value
    @discount.setter
    def discount(self, value: int):
        if not (0<value<=100):
            raise ValueError("Скидка должна быть от 0 до 100%")
        self.discount_value=value
    @property
    def final_price(self):
        final_price=self.price*(1-self.discount/100)
        return final_price
    @property
    def profit(self):
        profit=self.sell_price-self.buy_price
        return profit
   @property
    def profit_recent(self):
        try:
            profit_recent=(self.profit/self.buy_price)*100
            return profit_recent
        except ZeroDivisionError:
            raise ValueError("Цена покупки не должна быть 0")
    def __str__(self):
        return self.name
