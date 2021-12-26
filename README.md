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

## Implementing your own projects

### Import
You can import the module after installing by:
`import pythonp2p`

### Start
Firstly you need to extend the Node class and initialize the node:
```
  class Mynode(pythonp2p.Node):
    def on_message(self, message):
      # Gets called everytime there is a new message
  node = Mynode()
  node.start()
```

Advanced arguments:
`host`: The host where the socket run on. Default is "". Dont touch this if you dont have a weird network config.
`port`: the port where the nodes communicate. Default 65432
`file_server_port`: the port which the server for file transfer is listening on. It is optional. Default 65433

### Connection
To connect to a another node do:
`node.connect_to(ip)`

  `ip`: The other nodes ip. After this all other known peers to the other node will be sent to you to connect to.
  This is automatic.

`node.savestate()` save curent peers to a file.
  `file`: optional arg filename to save state to, default: state.json

`node.loadstate()` connect to previously discovered peers.
  `file`: optional arg filename to save state to, default: state.json

Note: You can also specify a `port` but it is not recommended since all of the network must run on the same port.

### Communication
To send data to the network you can do:
`node.send_message(data)`

`data`: a variable to be sent to all other nodes. It is recommended to use a dictionary for consistancy.

### Files

`node.setfiledir(path)` sets the directory in which files downloaded from the net will be stored.

`node.addfile(path)` or `pythonp2p.files.addfile(path)`: Adds a file to the node so it can be requested by others.

  `path`: The absolute path of the file in the computer.
  This function returns the hash which can be used by other nodes to request the file.

`node.requestFile(filehash)`: Send a request to the network and if the file is available, download it.

  `filehash`: The hash of the file to request in string format. Look above on `addfile` to get that.


## Commands
If running node.py directly you will need this.
- `msg` - send a message to all other connected peers.
- `req`- request a file by hash
- `add` - adds a file by path to be downloaded by other node.
- `refresh` - refresh all files in content/ directory and get their hashes to share wit ohers. This hash is used above.
- `peers` - Get a list of known peers and connected peers. Also their last ping.
- `connect` - The most important command. Use `connect someip` to connect to a node and join the network.
- `debug` - Toggles debug mode. I suggest you leave this on to debug issues.
- `exit` - Stop all threads and exit.

# Features

- When a node connects no another it will recieve a list of active node to connect to.
- Deticated file downloader and servr. When a node requests a file by its hash it will connect
to a node that has it and download it. Files can be shared by placing them in a specified directory and
will be detectd with a refresh. This can be expanded to become like torrents.
- Peer discovery. Every node gets a list of neighbours when connected.
- Messages run he entire network, so every node can get every info out there.
  This is not very good for big networks but it works on a small scale and sending
  rate can be edited for scale.

- Nodes ping eahother and decide if a node is dead.
- more idk read the code

# Issues
- mostly security. Do not use this for production, only fiddling around.
  I am not responsible if you get hacked because of security vulnerabillities here.
