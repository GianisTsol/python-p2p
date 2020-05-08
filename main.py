from node import peer
from node import *
from p2pnetwork.node import Node


peer.ConnectToNodes(1) # connect to the start node to enter the network
while 1:
    buf = str(peer.message({'msg': "test123"}))
    node.send_to_nodes(buf)
    time.sleep(2)

node.stop()
