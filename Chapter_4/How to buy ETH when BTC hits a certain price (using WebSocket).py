from KrakenKey import api_key, secret_key
import time, base64, hashlib, hmac, urllib.request, json
from websocket import create_connection
from time import sleep

api_nonce = bytes(str(int(time.time()*1000)), "utf-8")
api_request = urllib.request.Request("https://api.kraken.com/0/private/GetWebSocketsToken", b"nonce=%s" % api_nonce)
api_request.add_header("API-Key", api_key)
api_request.add_header("API-Sign", base64.b64encode(hmac.new(base64.b64decode(secret_key), b"/0/private/GetWebSocketsToken" + hashlib.sha256(api_nonce + b"nonce=%s" % api_nonce).digest(), hashlib.sha512).digest()))

token = json.loads(urllib.request.urlopen(api_request).read())['result']['token']
print(token)

try:
    ws = create_connection("wss://ws.kraken.com/")
    ws.send('{ "event": "subscribe", "pair": ["BTC/USD", "ETH/USD"], "subscription": { "name": "spread" }}')
except:
    print('Error')
   
    
while True:
    result = ws.recv()
    #print(result)
        
    if not "event" in result:
        if 'XBT/USD' in result:
            btc = float((result).split('"')[1])
            print(f'Bitcoin price: {btc}')

        if 'ETH/USD' in result:
            eth = float((result).split('"')[3]) + 2
            print(f'Ethereum price: {eth}')

        if btc >= 56400 and "ETH/USD" in result:
            ws.close()
            order_socket = create_connection("wss://ws-auth.kraken.com/")
            print(order_socket.recv())
            sleep(2)
            payload = {"event":"addOrder", "token":f"{str(token)}", 
                       "pair":"ETH/USD", "type":"buy", 
                        "ordertype":"limit", 
                        "price":f"{str(eth)}", "volume":"0.008", "userref":"42"}
            
            payload = str(payload).replace("'",'"')
            order_socket.send(payload)
            print(payload)
            
            sleep(1)
            
            order = order_socket.recv()
            print(f'###### \nOrder details: {order}')
            
            sleep(1)
            
            order = order.split(",")
            if '"status":"ok"' in order:
                print('##### \nOrder completed successfully!')
            else:
                print('##### \nOrder was rejected!')
            order_socket.close()
            break
            
        else:
            continue

