# python-p2p

A totaly decentralized python peer to peer network.

The code provides a simple network structure for information exchange between peers.

Using https://github.com/gryphius/port-forward for port forward by upnp.

# Install
note: tested on python 3.6+

To install the package do:
```
python setup.py install
```

## Implementing your own projects

### Import
You can import the module after installing by:
`import pythonp2p`

### Start
Firstly you need to initialize the node and then start it:
`node = pythonp2p.Node()
node.start()`

Advanced arguments:
`host`: The host where the socket run on. Default is "". Dont touch this if you dont have a weird network config.
`port`: the port where the nodes communicate. Default 65432
`file_server_port`: the port which the server for file transfer is listening on. It is optional. Default 65433

### Connection
To connect to a another node do:
`node.connect_to(ip)`

`ip`: The other nodes ip. After this all other known peers to the other node will be sent to you to connect to.
This is automatic.

Note: You can also specify a `port` but it is not recommended since all of the network must run on the same port.

### Communication
To send data to the network you can do:
`node.message(data)`

`data`: a dictionary to be sent to all other nodes. Please do not use `time`, `snid`, `req`, `resp` and `peers` as
dict keys as they are used by the network internally. You can use `msg` as a key to send strings. There is message filtering.

### Files

`node.addfile(path)` or `pythonp2p.files.addfile(path)`: Adds a file to the node so ith can be requested by others.

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
- `connect` - The most importsnt command. Use `connect [someip]` to connect to a node and join the network.
- `debug` - Toggles debug mode. I suggest you leave this on to debug issues.
- `exit` - Stop all threadsand exit.

# Features

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

# Issues
- mostly security. Do not use this for production, only fiddling around.
  I am not responsible if you get hacked because of security vulnerabillities here.
