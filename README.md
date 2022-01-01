[![build](https://github.com/GianisTsol/python-p2p/actions/workflows/python-package.yml/badge.svg)](https://github.com/GianisTsol/python-p2p/actions/workflows/python-package.yml)

# python-p2p

A totaly decentralized python peer to peer network.

The code provides a simple network structure for information exchange between peers.

Using https://github.com/gryphius/port-forward for port forward by upnp.

# Install
note: tested on python 3.8+

To install the package do:
```
python setup.py install
```

# Implementing your own projects

### Import
You can import the module after installing by:
`import pythonp2p`

## Start

Firstly you need to initialize the node and then start it. Look at blelow at [Receiving Data](#receiving-data) to learn how to extend he class first.

 #### Advanced arguments:


`host`: The host where the socket run on. Default is "". Dont touch this if you dont have a weird network config.

`port`: the port where the nodes communicate. Default 65432

`file_server_port`: the port which the server for file transfer is listening on. It is optional. Default 65433


## Connection
To connect to a another node do:
`node.connect_to(ip)`

  `ip`: The other nodes ip. After this all other known peers to the other node will be sent to you to connect to.
  This is automatic.
`port` : optional. default is the port the node is running on.


`Node.savestate(file)` save current peers to a file.

`Node.loadstate(file)` connect to previously discovered peers.

  `file`: optional arg filename to save/load state to/from, default: `state.json`

### Communication
 ### Sending data
To send data to the network you can do:
`node.send_message(data, receiver=None)`

`data`: a variable to be sent to all other nodes.

`receiver`: a string representing the id/public key of the node the message is for.
  If specified the message will be encrypted and only that node will be able to receive and read it.

 ### Receiving data

  To receive messages simply extend the Node class:

    class Mynode(Node):
      def on_message(message, sender, private):
        # Gets called everytime there is a new message
    node = Mynode()
    node.start()


  `message`: variable sent from other node.

  `sender`: a string representing the id/public key of the node that snt the message.

  `private`: bool representing if the message was encrypted and meant only for this node or public.


  ### Other node properties:
   `Node.id` : unique string identifying the node to the network, used to receive private messages.

## Files

`Node.setfiledir(path)` sets the directory in which files downloaded from the net will be stored.

`Node.addfile(path)` or `pythonp2p.files.addfile(path)`: Adds a file to the node so it can be requested by others.

  `path`: The absolute path of the file in the computer.
  This function returns the hash which can be used by other nodes to request the file.

`Node.requestFile(filehash)`: Send a request to the network and if the file is available, download it.

  `filehash`: The hash of the file to request in string format. Look above on `addfile` to get that.


# Features

- When a node connects no another it will receive a list of active node to connect to.
- File sharing. When a node requests a file by its hash it will connect
to a node that has it and download it. Files can be shared by adding adding them via command. This can be expanded to become like torrents.
- Peer discovery. Every node gets a list of neighbors when connected.
- Messages run he entire network, so every node can get every info out there.
  This is not very good for big networks but it works on a small scale and sending
  rate can be edited for scale.
 - Public key encryption so private messages can be sent.
 - Message signatures so no node van be impersonated.

- Nodes ping each other and decide if a node is dead.
- more idk read the code

# Issues
- mostly security. Do not use this for production, only fiddling around.
  I am not responsible if you get hacked because of security vulnerabilities here.
