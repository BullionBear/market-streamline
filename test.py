import asyncpg
import asyncio
from datetime import datetime

async def insert_order_update():
    # Convert the timestamp from milliseconds to a datetime object
    ts_datetime = datetime.utcfromtimestamp(1702952217421 / 1000.0)

    # Connection details
    conn = await asyncpg.connect(user='bullionbear', password='Sunshine4Jellybean',
                                 database='cryptostream', host='127.0.0.1')

    # Prepare data for 'a' and 'b' columns
    a_prices, a_sizes = zip(*[(1.0, 1.0), (2.0, 2.0)])
    b_prices, b_sizes = zip(*[(3.0, 1.0)])

    # Insert data into the table
    await conn.execute('''
        INSERT INTO order_updates (id, ex, base, quote, inst, ts, u, pu, a_price, a_size, b_price, b_size)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    ''', 10, 'binance', 'btc', 'usdt', 'spot', ts_datetime, 10, 0, a_prices, a_sizes, b_prices, b_sizes)

    # Close the connection
    await conn.close()

# Run the async function
asyncio.run(insert_order_update())