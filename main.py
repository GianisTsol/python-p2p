from node import Node
import time
import json
import sys
import data_request_management as dtrm
from file_transfer import FileDownloader
import portforwardlib
import hashlib


peers = []

msg_del_time = 30

PORT = 65432
FILE_PORT = 65433

requested = [] # list of files we have requested.
msgs = {} #hashes of recieved messages

portforwardlib.forwardPort(PORT, PORT, None, None, False, "TCP", 0, "", True)
portforwardlib.forwardPort(FILE_PORT, FILE_PORT, None, None, False, "TCP", 0, "", True)


def debugp(out):
    if node.debug == True:
        print("[debug] " + str(out))

def ConnectToNodes():
    for i in peers:
        if not node.connect_to(i, PORT):
            del peers[peers.index(i)] #delete wrong / own ip from peers

def message(dict, ex=[]):
    #time that the message was sent
    if "time" not in dict:
        dict['time'] = str(time.time())

    if "snid" not in dict:
        #sender node id
        dict['snid'] = str(node.id)

    if "msg" not in dict:
        dict['msg'] = "Automated data forward."

    node.network_send(dict, ex)

def req_file(fhash):
    message({'req': fhash})

def send_peers():
    global peers
    buf = {'peers': peers}
    message(buf)
    return

def data_handler(data, n):
    global peers
    global msgs
    dta = data
    if "peers" in dta:
        #peers handling
        for i in dta["peers"]:
            if i not in peers and i != "" and i != node.ip:
                peers.append(i)

        debugp("Known Peers: " + str(peers))
        ConnectToNodes() # cpnnect to new nodes
        return
    if "msg" in dta and "time" in dta:
        hash_object = hashlib.md5(dta["msg"].encode("utf-8"))
        msghash = str(hash_object.hexdigest())
        print(msghash)

        #check if the message hasn't expired.
        if float(time.time()) - float(dta['time']) < float(msg_del_time):
            if msghash not in msgs:
                msgs[msghash] = time.time()
                debugp("Incomig Message: " + dta["msg"])
                message(dta, ex=n)
            else:
                #debugp("expired:" + dta['msg'])
                if time.time() - msgs[msghash] > msg_del_time:
                    print(time.time() - msgs[msghash])
                    del msgs[msghash]
        else:
            #if message is expired
            debugp("expired:" + dta['msg'])

        if len(msgs) > len(peers) * 20:
            for i in msgs:
                if time.time() - msgs[i] > msg_del_time:
                    del msgs[i]
    if "req" in dta:
        if dtrm.have_file(dta['req']):
            message({"resp": dta['req'], "ip": node.ip, "localip": node.local_ip})
            debugp("recieved request for file: " + dta['req'] + " and we have it.")
        else:
            debugp("recieved request for file: " + dta['req'] + " but we do not have it.")

    if "resp" in dta and "snid" in dta and "ip" in dta:
        debugp("node: " + dta['snid']+" has file " + dta['resp'])
        if dta['resp'] in requested:
            print("node " + dta['snid'] + " has our file!")
            if dta['ip'] == "":
                if dta['localip'] != '':
                    downloader = FileDownloader(dta['localip'], FILE_PORT, str(dta['resp']))
                    downloader.start()
                    downloader.join()
            else:
                downloader = FileDownloader(dta['ip'], FILE_PORT, str(dta['resp']))
                downloader.start()
                downloader.join()

def node_callback(event, node, other, data):
    global peers

    if event == "node_disconnected":
        if other.host in peers:
            peers.remove(other.host)

    elif event == "node_connected":
        print(other.host)
        if other.host not in peers:
            peers.append(other.host)
        send_peers()

    elif event == "node_message":
        data_handler(data, [other.host, node.ip])

    else:
        print(event)

node = Node("", PORT, FILE_PORT, node_callback) # start the node
node.start()

def requestFile(fhash):
    requested.append(fhash)
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
        message({"msg": args})

    if cmd == "debug":
        node.debug = not node.debug
        print("Debug is now " + str(node.debug))

    if cmd == "stop":
        node.stop()


    if cmd == "exit":
        node.stop()
        portforwardlib.forwardPort(PORT, PORT, None, None, True, "TCP", 0, "PYHTON-P2P-NODE", True)
        portforwardlib.forwardPort(FILE_PORT, FILE_PORT, None, None, True, "TCP", 0, "PYHTON-P2P-FILESERVER", True)
        exit(0)

    if cmd == "refresh":
        dtrm.refresh()
        print(dtrm.f2data)

    if cmd == "peers":
        print("IP: " + node.ip)
        debugp(peers)
        print('--------------')
        for i in node.nodes_connected: print(i.id+' ('+ i.host + ') - ' + str(time.time() - int(i.last_ping)) + "s")
        if len(peers)==0: print("NO PEERS CONNECTED")
        print('--------------')

    if "req " in cmd:
        args = cmd.replace("req ", "")
        print("requesting file with hash: " + args)
        requestFile(args)
