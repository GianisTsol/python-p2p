# python-p2p

A totaly decentralized python peer to peer network.

The code provides a simple network structure for information exchange between peers.

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

- Peer discovery. Every node gets a list of neighbours when connected.
- Messages run he entire network, so every node can get every info out there.
  This is not very good for big networks but it works on a small scale and sending
  rate can be edited for scale.
  
- Nodes ping eahother and decide if a node is dead.
- more idk read the code

## Issues
- mostly security. Do not use this for production, only fiddling around.
  I am not responsible if you get hacked because of security vulnerabillities here.
