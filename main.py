print(str("""           ---Python p2p node by GTsol---
    Please make sure the latest version is installed
            older versions may contain bugs

 /\     /\\
{  `---'  }
{  O   O  }
~~>  V  <~~
 \  \|/  /
  `-----'____
  /     \    \_
 {       }\  )_\_   _
 |  \_/  |/ /  \_\_/ )
  \__/  /(_/     \__/
    (__/

    """))

from node import *
from p2pnetwork.node import Node

ConnectToNodes(1) # connect to the start node to enter the network
while 1:
    buf = str(message({'msg': "test123"}))
    node.send_to_nodes(buf)
    time.sleep(2)

node.stop()
