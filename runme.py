import argparse
import rest

if __name__ == "__main__":
    num_deauth_packets = 1
    parser = argparse.ArgumentParser(description="Tool to automate throwing deauth packets with the help of kismet")
    parser.add_argument("-u", "--username", required=True, help="Kismet username")
    parser.add_argument("-p", "--password", required=True, help="Kismet password")
    parser.add_argument("-i", "--iface", required=True, help="Interface that you want the deauth packets to be sent from")
    parser.add_argument("-c", "--count", type=int, default=num_deauth_packets, help=f"Number of deauth packets to throw, defaults to {num_deauth_packets}")

    args = parser.parse_args()

    print(f"Count: {args.count}")
    devices = rest.Devices(args.username, args.password, args.iface, args.count) 
