from pythonp2p import node
import pytest
import time

fhash = ""


node0 = node.Node("", 65434, 65436)
node1 = node.Node("", 65435, 65437)

node0.start()
node1.start()

node0.connect_to("127.0.0.1", 65435)


def test_node_connect():
    assert len(node0.nodes_connected) == 1
    assert len(node1.nodes_connected) == 1


def test_node_message():
    node0.send_message("node test")
    assert len(node1.msgs.keys()) == 1
    assert len(node0.msgs.keys()) == 1


def test_node_private_message():
    node0.send_message("TEST MESSAGE", reciever=node1.id)


def test_files_add():
    global fhash
    fhash = node1.addfile("LICENSE")


def test_file_request():
    node0.requestFile(fhash)
    print(node0.file_manager.getallfiles())
    assert len(node0.requested) == 1
    assert len(node1.msgs.keys()) == 2


node0.stop()
node1.stop()
