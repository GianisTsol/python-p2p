[![build](https://github.com/GianisTsol/python-p2p/actions/workflows/python-package.yml/badge.svg)](https://github.com/GianisTsol/python-p2p/actions/workflows/python-package.yml)

# python-p2p

A totally decentralized python peer to peer network.

The code provides a simple network structure for information exchange between peers.

Using https://github.com/gryphius/port-forward for port forward by upnp.

# Install
note: tested on python 3.9+

Install from pypi:
```
pip install pythonp2p
```

Install from source
```
pip install .
```

# Usage

#### Import
```py
from pythonp2p import Node
```

#### Start

 First, you need to initialize the node and then start it. Look at below at [Receiving Data](#receiving-data) to learn how to extend he class first.

 ```py
 node = Node(HOST, PORT, FILE_PORT)  # start the node
 node.start()
 ```


`HOST` (OPTIONAL): The host where the socket runs on. Don't touch this if you don't have a weird network config. Default is "".

`PORT` (OPTIONAL): The port where the nodes communicates. Default 65432

`FILE_PORT` (OPTIONAL): The port which the server for file transfer is listening on. Default 65433


#### Connection

```py
node.connect_to(ip)
```

`ip`: The other node's ip. After this all other known peers to the other node will be sent to you to connect to. This is automatic.


`port` (OPTIONAL): The default is the port the node is running on.

#### Saving state
Save current peers to a file.
```py
node.savestate(file)
```

Connect to previously discovered peers.
```py
node.loadstate(file)
```

`file` (OPTIONAL): filename to save/load state to/from, default: `state.json`

#### Communication
To broadcast data to the network you can do:
```py
node.send_message(data, receiver=None)
```

`data`: Dict to be sent to all other nodes.

`receiver`: A string representing the id/public key of the node the message is for.
  If specified the message will be encrypted and only that node will be able to receive and read it.



  To receive messages simply extend the Node class:
 
 ```py
 from pythonp2p import Node

 class Mynode(Node):
   def on_message(message, sender, private):
     # Gets called everytime there is a new message
 node = Mynode()
 node.start()
 ```


  `message`: variable sent from other node.

  `sender`: a string representing the id/public key of the node that snt the message.

  `private`: bool representing if the message was encrypted and meant only for this node or public.


#### node properties:
   `Node.id` : unique string identifying the node to the network, used to receive private messages.


#### Files

`Node.setfiledir(path)` sets the directory in which files downloaded from the net will be stored.

`Node.addfile(path)` or `pythonp2p.files.addfile(path)`: Adds a file to the node so it can be requested by others.

  `path`: The absolute path of the file in the computer.
  This function returns the hash which can be used by other nodes to request the file.

`Node.requestFile(filehash)`: Send a request to the network and if the file is available, download it.

  `filehash`: The hash of the file to request in string format. Look above on `addfile` to get that.


# How it works

- When a node connects no another it will receive a list of active node to connect to.
- File sharing. When a node requests a file by its hash it will connect
to a node that has it and download it. Files can be shared by adding adding them via command. This can be expanded to become like torrents.
- Peer discovery. Every node gets a list of neighbors when connected.
- Messages run the entire network, so every node can get every info out there.
  This is not very good for big networks but it works on a small scale and sending
  rate can be edited for scale.
 - Public key encryption so private messages can be sent.
 - Message signatures so no node van be impersonated.

- Nodes ping each other and decide if a node is dead.
- more idk read the code

# Issues
- mostly security. Do not use this for production, only fiddling around.
  I am not responsible if you get hacked because of security vulnerabilities here.
