import src.repository.bd as bd_repository
from datetime import datetime


def buy_product(product_bought):
  product_bought['event_time'] = datetime.utcnow(
  ).strftime('%Y-%m-%d %H:%M:%S UTC')

  rowcount = bd_repository.buy_product(product_bought)
  print(f'rowcount: {rowcount}')
