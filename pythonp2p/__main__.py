from .node import *

if __name__ == "__main__":
    new = Node("", PORT, FILE_PORT)  # start the node
    new.start()
    print("RUNNING IN CONSOLE MODE")
    try:
        while True:
            cmd = input("PYTHONP2P>")
            if cmd == "help":
                print(
                    """
                connect
                msg
                debug
                stop
                exit
                refresh
                add
                peers
                req
                load
                save
                """
                )
            if "connect " in cmd:
                args = cmd.replace("connect ", "")
                print("connect to: " + args)
                new.connect_to(args, PORT)

            if "msg " in cmd:
                args = cmd.replace("msg ", "")
                print("sent msg: " + args)
                new.message("msg", args)

            if cmd == "debug":
                new.debug = not new.debug
                print("Debug is now " + str(new.debug))

            if cmd == "stop":
                new.stop()

            if cmd == "exit":
                new.stop()
                exit(0)

            if cmd == "load":
                new.loadstate()

            if cmd == "save":
                new.savestate()

            if cmd == "refresh":
                new.file_manager.refresh()
                print(new.file_manager.files)

            if "add " in cmd:
                args = cmd.replace("add ", "")
                print("Adding file: " + args)
                try:
                    print(new.file_manager.addfile(args))
                    new.file_manager.refresh()
                except Exception as e:
                    print(e)

            if cmd == "peers":
                print("IP: " + new.ip)
                new.debug_print(new.peers)
                print("--------------")
                for i in new.nodes_connected:
                    print(
                        i.id
                        + " ("
                        + i.host
                        + ") - "
                        + str(time.time() - int(i.last_ping))
                        + "s"
                    )
                if len(new.peers) == 0:
                    print("NO PEERS CONNECTED")
                print("--------------")

            if "req " in cmd:
                args = cmd.replace("req ", "")
                print("requesting file with hash: " + args)
                new.requestFile(args)
    except Exception as e:
        new.stop()
        raise (e)
