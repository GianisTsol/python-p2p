# python-p2p

A totaly decentralized python peer to peer network.

The code provides a simple network structure for information exchange between peers.

Using https://github.com/gryphius/port-forward for port forward by upnp.

# Usage
#### Install requirements:
There ae no requirements yet, this is here for redundancy reasons.
```
pip install -r requirements.txt
```
note: tested on python 3.6
#### Start the node:
```
python main.py
```
## Features

- When a node connects no another it will recieve a list of active node to connect to.
- Deticated file downloader and servr. When a node requests a file by its hash it will connect
to a node that has it and download it. Files can be shared by placing the in the `content/` directory and the
will be detectd with a refresh. This can be expanded to become like torrents.
- Peer discovery. Every node gets a list of neighbours when connected.
- Messages run he entire network, so every node can get every info out there.
  This is not very good for big networks but it works on a small scale and sending
  rate can be edited for scale.

- Nodes ping eahother and decide if a node is dead.
- more idk read the code

## Issues
- mostly security. Do not use this for production, only fiddling around.
  I am not responsible if you get hacked because of security vulnerabillities here.

## Commands

- `msg` - send a message to all other connected peers.
- `req`- request a file by hash
- `refresh` - refresh all files in content/ directory and get their hashes to share wit ohers. This hash is used above.
- `peers` - Get a list of known peers and connected peers. Also their last ping.
- `connect` - The most importsnt command. Use `connect [someip]` to connect to a node and join the network.
- `debug` - Toggles debug mode. I suggest you leave this on to debug issues.
- `exit` - Stop all threadsand exit.

If this project gets enough stars Ill work on it and implement more features and security.
