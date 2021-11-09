# PORTFOLIO 1 - s344091
# server.py - TCP server
import socket,random,time,argparse

client = [] # client list
nameList = []
resp = [] # response list
action_list = ["walk", "sing", "jump", "cry", "fight", "steal", "cook", "print", "help"] # action list
verboseMode = False

def sendMsg(msg, clientSkip): # send msg to clients
    if clientSkip: # skip client
        for c in client:
            try:
                if c != clientSkip:
                    c.send(msg.encode())
                else:
                    c.send(msg.encode()+" (my response)".encode())
            except Exception as err: # client error
                clientError(c)
    else: # send to all
        for c in client:
            try:
                c.send(msg.encode())
            except Exception as err:
                clientError(c)

def getResp(): # fetch responses from clients
    for c in client:
        try:
            resp.append(c.recv(1024).decode()) # store response from clients
        except Exception as err:
            clientError(c)

def clientError(c):
    # remove client from list and send error msg
    global client
    client.remove(c)
    sendMsg("\nError: Oh no! A bot was disconnected:(", None)
    print("Error: A bot was disconnected.")

def chat(): # start new chat round
    global s
    action = random.choice(action_list) # random action

    if verboseMode:
        print("\n--- New chat round ---")
        print("Status: {} bots connected.".format(len(client)))
        print("Action: {}".format(action))

    if len(client) < 2: # minimum 2 clients must be connected.
        print("Error: 2 or more clients must be connected.")
        exit()

    while True:
        time.sleep(1)
        msg = "\nHost: Do you want to {}?".format(action)  # send to all bots
        print(msg)
        sendMsg(msg, None)

        index = 0

        for i in range(5):
            if index > len(client) - 1:
                index = 0
            time.sleep(1)
            getResp()
            print("Response from {}".format(resp[index]))
            sendMsg(resp[index], client[index])  # send respone to clients, not sender
            resp.clear()
            index += 1

        sendMsg("-- Chat round completed. Waiting on server... ", None)

        print("-- Chat completed. Start a new round? (Y / N)")
        restart = str(input())

        if restart.lower() == "y":
            getResp()
            resp.clear()
            action_list.remove(action)
            chat() # start new round
        else:
            print("Disconnecting clients...")
            for c in client:
                c.close()

            print("Server stopped! See you later;)")
            exit()

# parse terminal arguments
parser = argparse.ArgumentParser(description='Start chatserver. Eks: server.py 4242')
parser.add_argument('port', type=int, help='Port som server skal kjøre på. Må være heltall.')
parser.add_argument('-v', '--verbose', help='Vis debug info.', action='store_true')
args = parser.parse_args()
port = args.port

if args.verbose:
    verboseMode = True
    print("Host: localhost\nPort: {}\nSocket: SOCK_STREAM (TCP)\nStatus: listening...".format(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket over IPv4
s.bind(("localhost", port))  # bind to port
s.listen()  # listen for connections

print("\n--- TCP chat server running on localhost:{} --- \nWaiting for excatly 3 bots...\n".format(port))
print("--- Connected clients ---")

while True:
    # accept connection and add client
    conn, addr = s.accept()
    client.append(conn)
    num_clients = len(client)
    # get botname and print
    botName = conn.recv(1024).decode()
    print("{} - {}".format(botName, addr))
    # send welcome msg
    welcome = "Welcome {}!\n{} / 3 bot connected.".format(botName, num_clients)
    conn.send(welcome.encode())

    if num_clients == 3:
        chat() # start chat
        break