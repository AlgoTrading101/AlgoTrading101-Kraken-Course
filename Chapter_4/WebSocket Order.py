
from KrakenKey import api_key, secret_key
import time, base64, hashlib, hmac, urllib.request, json
from websocket import create_connection

api_nonce = bytes(str(int(time.time()*1000)), "utf-8")
api_request = urllib.request.Request("https://api.kraken.com/0/private/GetWebSocketsToken", b"nonce=%s" % api_nonce)
api_request.add_header("API-Key", api_key)
api_request.add_header("API-Sign", base64.b64encode(hmac.new(base64.b64decode(secret_key), b"/0/private/GetWebSocketsToken" + hashlib.sha256(api_nonce + b"nonce=%s" % api_nonce).digest(), hashlib.sha512).digest()))

token = json.loads(urllib.request.urlopen(api_request).read())['result']['token']

try:
    order_socket = create_connection("wss://ws-auth.kraken.com/")
    print(order_socket.recv())

    payload = {"event":"addOrder", "token":f"{str(token)}", 
                "pair":"ETH/USD", "type":"buy", 
                "ordertype":"limit", 
                "price":"2000", "volume":"0.008"}
            
    payload = str(payload).replace("'",'"')
    order_socket.send(payload)
    print(payload)
            
    time.sleep(1)
            
    order = order_socket.recv()
    print(f'###### \nOrder details: {order}')
except Exception as e:
    print("WebSocket Error")

order_socket.close()