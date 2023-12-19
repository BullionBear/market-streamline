INSERT_ORDER_UPDATE = '''
INSERT INTO order_updates (id, ex, base, quote, inst, ts, u, pu, a_price, a_size, b_price, b_size)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
'''
