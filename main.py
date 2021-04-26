from node import Node
import time
import json
import sys
import data_request_management as dtrm
from file_transfer import FileDownloader

peers = []

msg_del_time = 30

PORT = 65432
FILE_PORT = 65433

requested = [] # list of files we have requested.


def debugp(out):
    if node.debug == True:
        print("[debug] " + str(out))

def ConnectToNodes():
    for i in peers:
        node.connect_to(i, PORT)

def message(dict, ex=[]):
    #time that the message was sent
    dict['time'] = str(time.time())
    #sender node id
    dict['snid'] = str(node.id)

    node.network_send(dict, ex)

def req_file(hash):
    message({'req': hash})

def send_peers():
    global peers
    buf = {'peers': peers}
    message(buf)
    return

def data_handler(data, n):
    global peers
    dta = data
    if "peers" in dta:
        #peers handling
        for i in dta["peers"]:
            if i not in peers:
                peers.append(i)

        debugp("Known Peers: " + str(peers))
        ConnectToNodes() # cpnnect to new nodes
        return
    elif "msg" in dta and "time" in dta:
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
            message({"resp": dta['req'], "ip": node.ip})
        else:
            debugp("recieved request for file: " + dta['req'] + " but we do not have it.")

    elif "resp" in dta and "snid" in dta and "ip" in dta:
        debugp("node: " + dta['snid']+" has file " + dta['resp'])
        if dta['resp'] in requested:
            print("node " + dta['snid'] + " has our file!")
            downloader = FileDownloader(dta['ip'], FILE_PORT, hash)
            downloader.start()

    else:
        debugp("Recieved an unknown or corrupt message type.")

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


node = Node("", PORT, FILE_PORT, node_callback) # start the node
node.start()

def requestFile(hash):
    requested.append(hash)
    message({'req': args})

time.sleep(1)

while True:
    cmd = input(">")
    if "connect " in cmd:
        args = cmd.replace("connect ", "")
        print("connect to: " + args)
        node.connect_to(args, PORT)

    if "msg " in cmd:
        args = cmd.replace("msg ", "")
        print("sent msg: " + args)
        node.message({"msg": args})

    if cmd == "debug":
        node.debug = not node.debug
        print("Debug is now " + str(node.debug))

    if cmd == "stop":
        node.stop()


    if cmd == "exit":
        node.stop()
        exit(0)

    if cmd == "refresh":
        dtrm.refresh()

    if cmd == "peers":
        buf='--------------\n'
        for i in node.nodes_connected: buf = buf+'\n'+i.id+' ('+ i.host + ') - ' + str(time.time() - i.last_ping) + "s"
        if len(peers)==0: buf = buf + "NO PEERS CONNECTED\n"
        buf = buf + '\n--------------'
        print(buf)

    if "req " in cmd:
        args = cmd.replace("req ", "")
        print("requesting file with hash: " + args)
        requestFile(args)
