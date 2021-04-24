import threading
import uuid
import socket
from connection import *
import json

class Node(threading.Thread):
    def __init__(self, host, port, callback=None):

        self.terminate_flag = threading.Event()

        self.pinger = Pinger(self) # start pinger

        super(Node, self).__init__() #CAll Thread.__init__()

        self.callback = callback

        self.debug = True

        self.dead_time = 30 #time to disconect from node if not pinged

        self.host = host
        self.ip = host #own ip, will be changed by connection later
        self.port = port

        self.nodes_connected = []

        self.id = str(uuid.uuid4())

        self.max_peers = 10

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Initialisation of the Node on port: " + str(self.port) + " on node (" + self.id + ")")
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10.0)
        self.sock.listen(1)

    def debug_print(self, msg):
        if self.debug:
            print("[debug] " + str(msg))


    def network_send(self, message, exc=[]):
        for i in self.nodes_connected:
            if i.host in exc:
                pass
            else:
                i.send(json.dumps(message))

    def connect_to(self, host, port):

        if host == self.ip:
            self.debug_print("connect_to: Cannot connect with yourself!!")
            return False

        if len(self.nodes_connected) >= self.max_peers:
            self.debug_print("Peers limit reached.")
            return True

        for node in self.nodes_connected:
            if node.host == host:
                print("[connect_to]: Already connected with this node.")
                return True

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.debug_print("connecting to %s port %s" % (host, port))
            sock.connect((host, port))

            # Basic information exchange (not secure) of the id's of the nodes!
            sock.send(self.id.encode('utf-8')) # Send my id to the connected node!
            connected_node_id = str(sock.recv(4096).decode('utf-8')) # When a node is connected, it sends it id!

            thread_client = self.create_new_connection(sock, connected_node_id, host, port)
            thread_client.start()

            self.nodes_connected.append(thread_client)
            self.node_connected(thread_client)


        except Exception as e:
            self.debug_print("connect_to: Could not connect with node. (" + str(e) + ")")

    def create_new_connection(self, connection, id, host, port):
        return NodeConnection(self, connection, id, host, port)

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        self.pinger.start()
        while not self.terminate_flag.is_set():  # Check whether the thread needs to be closed
            try:
                connection, client_address = self.sock.accept()

                # Basic information exchange (not secure) of the id's of the nodes!
                connected_node_id = str(connection.recv(4096).decode('utf-8')) # When a node is connected, it sends it id!
                connection.send(self.id.encode('utf-8')) # Send my id to the connected node!

                thread_client = self.create_new_connection(connection, connected_node_id, client_address[0], client_address[1])
                thread_client.start()

                self.nodes_connected.append(thread_client)

                self.node_connected(thread_client)

            except socket.timeout:
                pass

            except Exception as e:
                raise e

            time.sleep(0.01)

        self.pinger.stop()
        for t in self.nodes_connected:
            t.stop()

        time.sleep(1)
        self.pinger.join()
        for t in self.nodes_connected:
            t.join()

        self.sock.close()
        print("Node stopped")

    def node_connected(self, node):
        self.debug_print("node_connected: " + node.id)
        if self.callback is not None:
            self.callback("node_connected", self, node, {})

    def node_disconnected(self, node):
        self.debug_print("node_disconnected: " + node.id)
        if self.callback is not None:
            self.callback("node_disconnected", self, node, {})


    def node_message(self, node, data):
        self.debug_print("node_message: " + node.id + ": " + str(json.loads(data)))
        if self.callback is not None:
            self.callback("node_message", self, node, json.loads(data))

class Pinger(threading.Thread):
    def __init__(self, parent):
        self.terminate_flag = threading.Event()
        super(Pinger, self).__init__() #CAll Thread.__init__()
        self.parent = parent
        self.dead_time = 30 #time to disconect from node if not pinged

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        while not self.terminate_flag.is_set():  # Check whether the thread needs to be closed
            for i in self.parent.nodes_connected:
                i.send('ping')
                time.sleep(20)
        print("Pinger stopped")
