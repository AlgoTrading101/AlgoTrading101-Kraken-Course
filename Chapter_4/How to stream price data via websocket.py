from websocket import create_connection
from time import sleep

ws = create_connection("wss://ws.kraken.com/")
ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD"]}')

while True:
    print(ws.recv())
    sleep(1)