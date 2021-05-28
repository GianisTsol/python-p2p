from pythonp2p import node
import pytest
import time

fhash = ""


node0 = node.Node("", 65434, 65436)
node1 = node.Node("", 65435, 65436)

node0.start()
node1.start()

node0.connect_to("127.0.0.1", 65435)

time.sleep(1)

def test_node_connect():
    assert len(node1.peers) == 1
    assert len(node0.peers) == 1
    assert len(node1.nodes_connected) == 1

time.sleep(1)
node0.message({'msg': "node test"})

def test_node_message():
    assert len(node1.msgs.keys()) == 1
    assert len(node0.msgs.keys()) == 0

def test_files_add():
    global fhash
    fhash = node0.addfile("./pythonp2p/content/test.txt")


def test_file_request():
    print("requesting file ... " + fhash)
    node1.requestFile(fhash)
    time.sleep(15)
    assert len(node0.msgs.keys()) == 1
    assert len(node1.msgs.keys()) == 2

node0.stop()
node1.stop()
