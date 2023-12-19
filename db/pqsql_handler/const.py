INSERT_ORDERBOOK = '''
INSERT INTO orderbook(id, timestamp, exchange, instrument, symbol) 
VALUES($1, to_timestamp($2), $3, $4, $5)
'''

INSERT_DEPTH = '''
INSERT INTO depth(id, layer, side, price, vol) 
VALUES($1, $2, $3, $4, $5)
'''
