from node import Node
import time
import json
import sys
import data_request_management as dtrm

peers = []

msg_del_time = 30

PORT = 65432

def debugp(out):
    if node.debug == True:
        print("[debug] " + str(out))

def ConnectToNodes():
    for i in peers:
        node.connect_to(i, PORT)

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
        for i in dta["peers"]:
            if i not in peers:
                peers.append(i)

        debugp("Known Peers: " + str(peers))
        ConnectToNodes() # cpnnect to new nodes
        return
    elif "msg" in dta:
        #handle message data.
        debugp("Incomig Message: " + dta["msg"])
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
        debugp("node: " + dta['snid']+" has file " + dta['resp'])
        debugp("Downloading files will be added in another version (probably never lol the dev sucks)")

def node_callback(event, node, other, data):
    global peers
    if event == "node_disconnected":
        if other.host in peers:
            peers.remove(other.host)

    elif event == "node_connected":
        if other.host not in peers:
            peers.append(node.host)
        send_peers()

    elif event == "node_message":
        data_handler(data, [other.host, node.ip])

    else:
        print(event)


node = Node("", PORT, node_callback) # start the node
node.start()

while True:
    cmd = input(">")
    if "connect " in cmd:
        args = cmd.replace("connect ", "")
        print("connect to: " + args)
        node.connect_to(args, PORT)

    if "msg " in cmd:
        args = cmd.replace("msg ", "")
        print("sent msg: " + args)
        node.network_send({"msg": args})

    if cmd == "debug":
        node.debug = not node.debug
        print("Debug is now " + str(node.debug))

    if cmd == "stop":
        node.stop()


    if cmd == "exit":
        node.stop()
        exit(0)

    if cmd == "peers":
        buf='--------------\n'
        for i in node.nodes_connected: buf = buf+'\n'+i.id+' -|- '+i.host
        if len(peers)==0: buf = buf + "NO PEERS CONNECTED\n"
        buf = buf + '\n--------------'
        print(buf)

    if "msg " in cmd:
        args = cmd.replace("msg ", "")
        print("message: " + args)
        message({'msg': args})

    if "req " in cmd:
        args = cmd.replace("req ", "")
        print("requesting file with hash: " + args)
        message({'req': args})
