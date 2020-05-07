#simple python peer to peer network using the p2pnetwork module. It uses a simple model for information exchange between peers.
# Author: Giannis Tsolakis
# no liscence do whatever you want

from p2pnetwork.node import Node
import time
import json
import sys

peers = ['192.168.1.6']
node1 = None
sys.path.insert(0, '.')


def data_handler(data):
    global peers
    dta = data
    #dta = {'test': 'lol'}
    dta = json.loads(data)
    if "peers" in dta:
        new = [i for i in peers if i not in dta["peers"]]
        peers = dta["peers"] + new
        print("new neighbours: " + str(new))
    elif "msg" in dta:
        print("msg: " + dta["msg"])


def message(dict):
    #print(dict)
    buf = json.dumps(dict)
    return buf

def peers_packet():
    global peers
    buf = {'peers': peers}
    buf = json.dumps(buf)
    return buf


def node_callback(event, node, other, data):
    if (event == 'node_request_to_stop'):
        print("node request to stop")
    #if event != 'node_request_to_stop': # node_request_to_stop does not have any connected_node, while it is the main_node that is stopping!
    #    print('Event: {} from main node {}: connected node {}: {}'.format(event, node.id, other.id, data))
    elif ( event == "inbound_node_disconnected" ):
        print("NODE (" + node.getName() + "): " + "event:" + event + "\n")
    elif ( event == "outbound_node_disconnected" ):
        print("NODE (" + node.getName() + "): " + "event:" + event + "\n")
    elif ( event == "outbound_node_connected" ):
        print("NODE (" + node.getName() + "): " + "event:" + event + "\n")
    elif ( event == "inbound_node_connected" ):
        print("NODE (" + node.getName() + "): " + "event:" + event + "\n")
    elif ( event == "node_message" ):
        #print("NODE (" + node.getName() + "): " + "event:" + event + ": " + "data: " + str(data) + "\n")
        #print(data)
        data_handler(data.encode('utf-8'))
    else:
        print("NODE (" + node.getName() + "): Event is not known " + event + "\n")


# Just for test we spin off multiple nodes, however it is more likely that these nodes are running
# on computers on the Internet! Otherwise we do not have any peer2peer application.
node_1 = Node("127.0.0.1", 8001, node_callback)
node_2 = Node("127.0.0.1", 8002, node_callback)
node_3 = Node("127.0.0.1", 8003, node_callback)


node_1.start()
node_2.start()
node_3.start()
time.sleep(1)

node_1.connect_with_node('127.0.0.1', 8002)
node_2.connect_with_node('127.0.0.1', 8003)
node_3.connect_with_node('127.0.0.1', 8001)

time.sleep(1)

while 1:
    buf = str(message({'msg': "lloolll"}))
    node_2.send_to_nodes(buf)
    node_2.send_to_nodes(peers_packet())
    #node_1.send_to_nodes("lolllllllllllllll")
    time.sleep(1)
time.sleep(5)

node_1.stop()
node_2.stop()
node_3.stop()

print('end')
