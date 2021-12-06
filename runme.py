import argparse
import rest
import datetime
import logging
import os

#TODO - ID random MAC


def read_contents(file_path):
    if not os.path.isfile(file_path):
        print(f"{file_path} is not a FILE")
        exit(-1)
 
    with open(file_path) as f:
        return f.readlines()

if __name__ == "__main__":
    num_deauth_packets = 1
    whitemacs = []
    whitessid = []
    blackmacs = []
    blackssid = []

    parser = argparse.ArgumentParser(description="Tool to automate throwing deauth packets with the help of kismet. Logs will go to deauther.log.  If a white list is desired, create a folder for macs and a separate folder for ssids.  These folders should contain one value per line, no commas. Use the -w or -s option to point the program at these files, respectively")
    parser.add_argument("-u", "--username", required=True, help="Kismet username")
    parser.add_argument("-p", "--password", required=True, help="Kismet password")
    parser.add_argument("-i", "--iface", required=True, help="Interface that you want the deauth packets to be sent from")
    parser.add_argument("-c", "--count", type=int, default=num_deauth_packets, help=f"Number of deauth packets to throw, defaults to {num_deauth_packets}")
    parser.add_argument("-w", "--whitemac", default=None, required=False, help="Path to file of white list of MAC addresses that you dont want deauth-ed (client or AP)")
    parser.add_argument("-s", "--whitessid", default=None, required=False, help="Path to file of white list of SSID addresses that you dont want deauth-ed")
#    parser.add_argument("-b", "--blackmac", default=None, required=False, help="Path to file of black list of the ONLY MAC addresses that you want targeted (client or AP)")
#    parser.add_argument("-d", "--blackssid", default=None, required=False, help="Path to file of black list of the ONLY SSIDs that you want targeted")

    args = parser.parse_args()

    if args.whitemac:
        whitemacs = read_contents(args.whitemac)

    if args.whitessid:
        whitessid = read_contents(args.whitessid)

#    if args.blackmac:
#        blackmacs = read_contents(args.blackmac)

#    if args.blackssid:
#        blackssids = read_contents(args.blackssid)

    logging.basicConfig(filename="example.log", level=logging.DEBUG)

    logging.debug(f"#############{str(datetime.datetime.now())}###########")
    logging.debug(f"Calling devices: username={args.username}, password={args.password}, interface={args.iface}, count: {args.count}")
    devices = rest.Devices(args.username, args.password, args.iface, args.count, white_mac=whitemacs, white_ssid=whitessid, black_mac=blackmacs, black_ssid=blackssid) 
    devices.get_access_points()
