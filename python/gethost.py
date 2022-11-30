import sys
import socket

def main() -> None:
    if len(sys.argv) > 1:
        print("\u001b[37;1m"+socket.gethostbyaddr(sys.argv[1])[0]+"\u001b[0m")

if __name__ == "__main__":
    main()
