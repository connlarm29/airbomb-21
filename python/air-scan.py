#/usr/lib/python3
"""Port scanning tool for discovering Apple TVs on a network.
Don't mind the spaghetti in the code, its free snacks.
"""

import socket
import sys

# addr = socket.gethostbyname(socket.gethostname()).rsplit('.',2)[0]+'.'
try:
    tmp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmp_sock.connect(("10.255.255.255",1))
    addr = tmp_sock.getsockname()[0].rsplit('.',2)[0]+'.'
except Exception:
    print("Err: Could not resolve local IP.")
    exit()
finally:
    tmp_sock.close()


tv_list = []
PORT = 5000
MODE = "w"
#Arg parsing stuff
NETWORK_ID= ""
CUSTOM_NETWORK_ID = False
VERBOSE_MODE = False

for arg in sys.argv:
    if arg == "air-scan.py" or arg.isdigit():
        "do nothing"
    elif arg == "-a":
        MODE = "a"
    elif arg == "-v":
        VERBOSE_MODE = True
    elif arg == "-h":
        print("""
[]================================[]
|||Network Scanner for Air-Raid.py||
||================================||
|| -v : VERBOSE mode, extra info  ||
||                                ||
|| -n [id] : NETWORK ID, specify  ||
||           custom network ID    ||
||                                ||
|| -h : HELP, prints this page    ||
||                                ||
|| -a : APPEND, append to file    ||
[]================================[]
        """)
        exit()
    elif arg == "-n":
        if len(sys.argv) > sys.argv.index("-n")+1 and \
        sys.argv[sys.argv.index("-n")+1].isdigit():
            if int(sys.argv[sys.argv.index("-n")+1]) < 0 or \
             int(sys.argv[sys.argv.index("-n")+1]) > 255:
                print("Invalid Network ID!")
                exit()
            else:
                CUSTOM_NETWORK_ID = True
                NETWORK_ID = sys.argv[sys.argv.index("-n")+1]
        else:
            print("No network ID provided, scanning all")
    else:
        print("Invalid Arguement, use '-h' for help.")
        exit()


def main():  

    print("\nX===========================================X")
    print("Beginning port scan on port {}\n".format(PORT))

    netscanner = network_scanner()
    
    #acutal scanning stuff
    for network_id in range(1,256):
        if CUSTOM_NETWORK_ID: network_id = NETWORK_ID
        print("\u001b[36;1m===> Scanning IP range "+addr+str(network_id)+".*\u001b[0m")
        for host_id in range(1,256):
            target_addr = addr+str(network_id)+"."+str(host_id)
            if VERBOSE_MODE:
                if CUSTOM_NETWORK_ID: print("checking device " \
                + target_addr + "[{}/{}]".format(host_id,256))
                else: print("checking device " + target_addr \
                + "[{}/{}]".format(host_id*network_id,256*256))
            try:
                if netscanner.scan_port(target_addr,PORT):
                    tv_list.append(target_addr)
            except KeyboardInterrupt:
                print("Exiting..\n")
                exit()
        if CUSTOM_NETWORK_ID: break;

    print("\nX===========================================X\n")
    
    #formatting and output to file
    if len(tv_list) == 0:
        print("\u001b[32;1m[!]\u001b[0m No Devices Found, exiting...")
        exit()
    for device in tv_list:
        try:    
            print("\u001b[32;1m[!]\u001b[0m Possible Apple TV device at: "\
            +device + " ... \u001b[37;1m" + socket.gethostbyaddr(device)[0] + "\u001b[0m")
        except socket.herror:
            print("\u001b[32;1m[1]\u001b[0m Port is open, but could not resolve hostname for " + device) 
    with open("airraid_targets",MODE) as output:
        for device in tv_list:
            output.write(device+"\n")
    print("Wrote targets to 'arraid_targets' file for use in air-raid.py!")
    exit()        

#helper class that wraps the port-scanning magic
class network_scanner:

    def scan_port(self,ip: str, port: int) -> bool:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.01)
            result = s.connect_ex((ip,port))
            if result == 0:
                print("\u001b[32;1m[~]\u001b[0mDevice " + \
                ip + " has port {} OPEN!".format(port))
                return True;
            s.close()
        except socket.gaierror:
            print("E: Could not resolve hostname...\n")
        except socket.error:
            print("E: No response from target...\n")
        return False


if __name__ == "__main__":
    main()
