# kismet_deauth
Automated deauth tool, targets sourced from kismet

Currently run with 1 alfa card.
./run_me.py -h

need the kismet username and password. to set the username and password, browse to the kismet server (www.localhost:2501) that you are running.  Once set, the creds are stored in ~/.kismet/kismet_httpd.conf (https://www.kismetwireless.net/docs/readme/webserver/)

required args are:
username
password
interface (to send the deauth packet from)
