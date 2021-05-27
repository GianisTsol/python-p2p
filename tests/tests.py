from .. import node

node0 = node.Node(port=65434)
node1 = node.Node(port=65435)

node0.start()
node1.start()
