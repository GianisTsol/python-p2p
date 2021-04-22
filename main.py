from node import Node
import time
import json
import sys
import data_request_management as dtrm

peers = []

msg_del_time = 30

PORT = 65432

def debugp(out):
    if node.debug_mode == True:
        print("\033[93m [debug] " + str(out) + " \033[0m")

def response(out):
        print("\033[92m" + str(out) + " \033[0m")

def ConnectToNodes():
    for i in peers:
        node.connect_to(i)

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
        node.network_send(buf, ex)

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

        debugp("Own ip: " + myip)
        if myip in new:
                new.remove(myip) # remove your ip so it will not connect to itself
        #print("new neighbours: " + str(new))
        debugp("peers: " + str(peers))
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
            debugp("expired:" + dta['msg'])
        return
    elif "req" in dta:
        if dtrm.have_file(dta['req']):
            message({"resp": hash})

        else:
            debugp("recieved request for file: " + dta['req'] + " but we do not have it.")

    elif "resp" in dta:
        debug("node: " + dta['snid']+"has file " + dta['resp'])
        debugp("Downloading files will be added in another version (probably never lol the dev sucks)")

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
node.start()

while True:
    cmd = input(">")
    if "connect " in cmd:
        args = cmd.replace("connect ", "")
        response("connect to: " + args)
        node.connect_to(args, PORT)

    if "msg " in cmd:
        args = cmd.replace("msg ", "")
        response("sent msg: " + args)
        node.network_send({"msg": args})

    if cmd == "debug":
        node.debug = not node.debug
        response("Debug is now " + str(node.debug))

    if cmd == "stop":
        node.stop()


    if cmd == "exit":
        node.stop()
        exit(0)

    if cmd == "peers":
        response(peers)

    if "msg " in cmd:
        args = cmd.replace("msg ", "")
        response("message: " + args)
        message({'msg': args})

    if "req " in cmd:
        args = cmd.replace("req ", "")
        response("requesting file with hash: " + args)
        message({'req': args})
