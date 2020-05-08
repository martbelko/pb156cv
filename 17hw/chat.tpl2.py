#!/usr/bin/python3

import socket
import sys
import os
import selectors

def color_handler(command, payload):
    escape = "\033[m"
    colors = {
        "black": "\033[0m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "white": "\033[37m",
    }
    
    print((colors[command] if command in colors else escape) + payload + escape)

def quit_handler(_, __):
    sys.exit(0)

def whoami_handler(_, __):
    user = os.environ['USER'] if 'USER' in os.environ else os.environ['USERNAME'] if 'USERNAME' in os.environ else 'unknown'
    print("The oracle claims you are " + username)

commands = {
    'whoami': whoami_handler,
    'quit':    quit_handler,
    'exit':    quit_handler,
    'leave': quit_handler,
    'red': color_handler,
    'blue': color_handler,
    'green': color_handler,
    'yellow': color_handler,
    'white': color_handler,
    'purple': color_handler,
    'black': color_handler,
}

def process(commandline):
    commandline = commandline.rstrip("\n\r")
    splitted = commandline.split(" ", 1)
    if not splitted:
        return

    cmdkey = splitted[0]
    if not cmdkey.startswith("\\"):
        print(commandline)
        return

    cmdkey = cmdkey[1:]
    if not cmdkey in commands:
        print(commandline)
        return

    commands[cmdkey](cmdkey, splitted[1] if len(splitted) > 1 else "")

def client(proto, host, port):
    """
        Ok, this function should make sense of proto (string tcp or udp),
        host and port.
        
        Then it should continue send / read messages until user enters one of terminal commands
    """

    def net_read(_, sock):
        # network reading here 
        remotedata = None # todo socket read here
        remoteline = remotedata.decode('utf-8')
        process(remoteline)

    def input_read(stdi, sock):
        commandline = stdi.readline()
        process(commandline)
        localdata = bytes(commandline, 'utf-8')
        # network write here

    multiplexer = selectors.DefaultSelector()
    # todo: somebody should probably do some networking here
    # todo: perhaps name resolving support?
    # sock is the network socket
    # perhaps set socket as non-blocking? Not needed on some systems

    multiplexer.register(sock, selectors.EVENT_READ, net_read)
    multiplexer.register(sys.stdin, selectors.EVENT_READ, input_read)
    while True:
        ready = multiplexer.select()
        for key,_ in ready:
            callback = key.data
            callback(sys.stdin, sock)


if __name__ == "__main__":
    proto = sys.argv[3] if len(sys.argv) >= 4 else "tcp"    
    host = sys.argv[1] if len(sys.argv) >= 2 else "147.251.54.177"
    port = sys.argv[2] if len(sys.argv) >= 3 else "10000" if proto == "udp" else "10001"

    client(proto, host, port)