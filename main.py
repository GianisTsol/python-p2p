import os

os.system("cls")

print(str("""
           ---Python p2p node by GTsol---
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
import time

try:
    node.start()
except KeyboardInterrupt:
    node.stop()
    exit(0)
