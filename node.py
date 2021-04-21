#simple python peer to peer network using the p2pnetwork module. It uses a simple model for information exchange between peers.
# Author: Giannis Tsolakis
# no liscence do whatever you want

from p2pnetwork.node import Node
import time
import json
import sys
from requests import get
import data_request_management as dtrm

#don't have to add a lot of peers
peers = {}
# The maximum amount of peers that can connect to the node
maxpeers = 5
# Currently connected peers
connected_peers = 0
#time to wait until a message will stop being forwarded - in seconds
msg_del_time = 30
# The port that the server will run on.
#To form a single network, please, do not change this
PORT = 65432

###########################################################

#your ip that others connect to
myip = ''
#uncomment these two lines to get public ip from external server.
#myip = get('https://api.ipify.org').text
#print("Public IP: " + myip)


def ConnectToNodes(nn):
    global connected_peers
    global peers
    global maxpeers
    if connected_peers+nn>maxpeers:
        nn = maxpeers-connected_peers
    if connected_peers >= maxpeers:
        print("FUCK FUCK FUCK, too much peers, how did this happen?? fuck")
        return
    if nn > len(peers):
        nn = len(peers)
    for i in range(nn):
        print('connecting with {}'.format(peers[i]))
        node.connect_with_node(peers[i], PORT)
    return

def message(dicts, ex=[]):
    dict = {}
    dict = dicts
    #time that the message was sent
    dict['time'] = str(time.time())
    #sender node id
    if node != None:
        dict['snid'] = str(node.id)
    buf = json.dumps(dict)
    if node != None:
        node.send_to_nodes(buf, ex)

def req_file(hash):
    message({'req': hash})

def send_peers():
    global peers
    buf = {'peers': peers}
    message(buf)
    return

def data_handler(data, n):
    global peers
    dta = {}
    dta = json.loads(data)
    if "peers" in dta:
        #peers handling
        new = {}
        for i in dta["peers"]:
            if i not in peers:
                new = {**peers, **new}

        print("Own ip: " + myip)
        if myip in new:
                new.remove(myip) # remove your ip so it will not connect to itself
        #print("new neighbours: " + str(new))
        print("peers: " + str(peers))
        ConnectToNodes(len(new)) # cpnnect to new nodes
        return
    elif "msg" in dta:
        #handle message data.
        print(time.ctime() + " msg: " + dta["msg"])
        #check if the message hasn't expired.
        if float(time.time()) - float(dta['time']) < float(msg_del_time):
            message(dta, ex=n)
        else:
            #if message is expired
            print("expired:" + dta['msg'])
        return
    elif "req" in dta:
        if dtrm.have_file(dta['req']):
            message({"resp": hash})

        else:
            print("recieved request for file: " + dta['req'] + " but we do not have it.")

    elif "resp" in dta:
        print("node: " + dta['snid']+"has file " + dta['resp'])
        print("Downloading files will be added in another version")

def node_callback(event, node, other, data):
    global connected_peers
    print("connected peers: " + str(connected_peers))
    global peers
    print(event + "\n")
    if ("disconnected" in event):
        if node.nodeip in peers:
            peers.remove(node.nodeip)
        print(event + "\n")
        connected_peers = connected_peers -1
    elif ("connected" in event):
        if other.id == node.id:
            myip = node.nodeip
            print("connected to ourselves, ip: " + node.nodeip)
            if node.nodeip in peers:
                peers.remove(node.nodeip)
            node.disconnect_with_node(other)
        if (event=="inbound_node_connected"):
            send_peers()

        if (event=="outbound_node_connected"):
            send_peers()
        print("the node's address is: " + str(node.nodeip))
        if node.id not in peers:
            peers[node.id] = (node.nodeip)
        connected_peers = connected_peers +1
    elif ( event == "node_message" ):
        data_handler(data, [other, node])
    else:
        print(event)

    print(peers)

node = Node("", PORT, node_callback) # start the node

while True:
    cmd = input(">")
    if "connect " in cmd:
        args = cmd.replace("connect ", "")
        print("connect to: " + args)
        node.connect_with_node(args, PORT)

    if cmd == "stop":
        node.stop()

    if cmd == "exit":
        node.stop()
        exit(0)

    if cmd == "peers":
        print(peers)

    if "msg " in cmd:
        args = cmd.replace("msg ", "")
        print("message: " + args)
        message({'msg': args})

    if "req " in cmd:
        args = cmd.replace("req ", "")
        print("requesting file with hash: " + args)
        message({'req': args})
