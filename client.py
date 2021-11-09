# PORTFOLIO 1 - s344091
# client.py
import socket,random,argparse

verb = None
badVerb = None
next = None

def bot(data, name):

    global verb, badVerb, next

    # parse string
    words = data.split()
    action = words[-1]
    action = action[:-1]
    sender = words[0]
    sender = sender[:-1]

    # actions
    bad = ["cry", "fight", "steal"]
    good = ["walk", "sing", "jump"]

    if sender == "Host": # respond to host
        verb = action
        next = 1
        if action in bad: # bad action
            badVerb = True
            return "{}: Yes! I have been thinking about {}ing all week.".format(name, action)
        elif action in good: # good action
            badVerb = False
            return "{}: No! {}ing sounds super boring.".format(name, action)
        else: # undefined action
            badVerb = None
            return "{}: I don't care about {}ing!".format(name, action)
    elif next == 1: # bot 2 response
        next = 2
        if badVerb: # bad action
            return "{}: What is wrong with you {}?? {}ing sounds horrible...".format(name, sender, verb)
        elif badVerb is None: # undefined action
            return "{}: {}ing sounds alright. But I don't mind doing something else...".format(name, verb)
        elif not badVerb: # good action
            return "{}: {}ing sounds fun! But I want more choices!".format(name,verb)
    elif next == 2: # bot 3 response
        next = 3
        alt = random.choice(["running", "skiing", "reading"])
        return "{}: I agree with {}. Lets do some {} instead!".format(name, sender, alt)
    elif next == 3: # bot 1 response
        next = 4
        if badVerb: # bad action
            return "{}: But I really enjoy {}ing!".format(name, verb)
        elif badVerb is None: # undefined action
            return "{}: Sure. We can always do that.".format(name)
        elif not badVerb: # good action
            return "{}: Yes! Excellent choice {};)".format(name,sender)
    elif next == 4: # bot 2 response
        resp = random.choice(["I'm getting tired. Good night.", "I wonder what the meaning of life is... Maybe, cake?", "Fun fact! Pringles aren't actually potato chips."])
        return "{}: {}".format(name, resp)

parser = argparse.ArgumentParser(description='Koble til chatserver. Eks: client.py localhost 4242 Joe')
parser.add_argument('host', type=str, help='Server som bot skal koble til.')
parser.add_argument('port', type=int, help='Port som bot skal koble til. Må være heltall.')
parser.add_argument('bot', type=str, help='Navnet på bot.')
args = parser.parse_args()
host = args.host
port = args.port
botName = args.bot

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port)) # connect to host

s.send(botName.encode()) # send botname to host
welcome = s.recv(1024).decode() # recv welcome message
print(welcome)

while True:
    try:
        data = s.recv(1024).decode() # recv from host
        print(data)
        resp = bot(data, botName) # parse string and create response
        s.send(resp.encode()) # send response
    except Exception as e:
        print("\nYou have been disconnected.")
        break
