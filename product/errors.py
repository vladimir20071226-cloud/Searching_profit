class InsufficientStockError(Exception):
    def __init__(self, product_name:str, requested:int, available:int):
        self.product_name=product_name
        self.requested=requested
        self.available=available
        super().__init__(f'Товар {self.product_name}: запрошено {self.requested}, в наличии только{self.available}')