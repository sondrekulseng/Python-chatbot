<img src="https://drive.google.com/thumbnail?id=10MLLfi0yYpP0EZF3M7xVTN2Byc3pCZAm" alt="Logo" width="120"/>

# Python-chatbot

This was an individual project in the course "DATA2410 Networking and cloud computing" at OsloMet. <br />
The task was to create Python chatbots that could talk to eachother via. a socket API.

## How to run:
In this project there are two Python files:
  - **server.py: Used to host the chat session.**
    - Requires port number as argument:
      ```console
      python3 server.py 4242
      ```
    - Type **server.py --h** for more info:
      ```console
      usage: server.py [-h] [-v] port

      Start chatserver. Eks: server.py 4242

      positional arguments:
      port           Port som server skal kjøre på. Må være heltall.

      optional arguments:
        -h, --help     show this help message and exit
        -v, --verbose  Vis debug info.

      ```
  - **client.py: The bots.**
    - Requires hostname, port number and bot name as arguments. The bot name can be whatever you want.
      ```console
      python3 client.py localhost 4242 Bob
      ```
    - Type **client.py --h** for more info:
      ```console
      usage: client.py [-h] host port bot

      Koble til chatserver. Eks: client.py localhost 4242 Joe

      positional arguments:
        host        Server som bot skal koble til.
        port        Port som bot skal koble til. Må være heltall.
        bot         Navnet på bot.

      optional arguments:
        -h, --help  show this help message and exit
      ```

