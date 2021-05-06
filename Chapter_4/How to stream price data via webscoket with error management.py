from websocket import create_connection

try:
    ws = create_connection("wss://ws.kraken.com/")
    ws.send('{ "event": "subscribe", "pair": ["XBT/USD"], "subscription": { "name": "ohlc", "interval":5 }}')
except Exception as e:
    print('Error')

while True:
    try:
        print((ws.recv()))
    except Exception as e:
        print('Error fetching data')