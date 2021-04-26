import threading
import socket
import pickle
import data_request_management as dtrm
import time
import struct
import json
import miniupnpc

class fileClientThread(threading.Thread):
    def __init__(self, ip, port, conn, file_requested):
        super(fileClientThread, self).__init__() #CAll Thread.__init__()
        self.terminate_flag = threading.Event()
        self.ip = ip
        self.port = port
        self.sock = conn
        self.file_requested = file_requested

    def SendFile(self, filehash):
        j = open("resources.json", "rb")
        content = json.load(j)
        j.close()
        filehash = str(filehash)
        if not dtrm.have_file(filehash):
            print('File requested to download but we do not have: ' + filehash)
            self.sock.close()
        else:
            file = content[filehash]
            f = open(file, 'rb')
            data = f.read()
            serialized_data = pickle.dumps(data)
            self.sock.sendall(struct.pack('>I', len(serialized_data)))
            self.sock.send(file.encode('utf-8'))
            self.sock.sendall(serialized_data)

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        self.SendFile(self.file_requested)
        time.sleep(0.05)
        self.sock.close()

class fileServer(threading.Thread):
    def __init__(self, parent, PORT):
        self.terminate_flag = threading.Event()
        super(fileServer, self).__init__() #CAll Thread.__init__()

        self.parent = parent
        self.port = PORT

        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 10
        upnp.discover()
        upnp.selectigd()
        # addportmapping(external-port, protocol, internal-host, internal-port, description, remote-host)
        upnp.addportmapping(self.port, 'TCP', upnp.lanaddr, port, 'PYTHON-P2P-FILESERVER', '')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(10.0)
        self.sock.bind(("", self.port))
        self.sock.listen(1)

        self.threads = []

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        print("File Server Started")
        while not self.terminate_flag.is_set():  # Check whether the thread needs to be closed
            try:
                (conn, (ip, port)) = self.sock.accept()

                self.parent.debug_print('File Server conection from: '+ str(ip))

                file_requested = str(conn.recv(4096).decode('utf-8')) #recieve file hash

                newthread = fileClientThread(ip, port, conn, file_requested)
                dtrm.refresh()
                newthread.start()

                self.threads.append(newthread)

            except socket.timeout:
                pass

            except Exception as e:
                raise e
        time.sleep(0.01)

        for t in self.threads:
            t.join()
        print("File Server stopped")

class FileDownloader(threading.Thread):
    def __init__(self, ip, port, hash):
        super(FileDownloader, self).__init__()

        self.hash = str(hash)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(10.0)
        self.conn.connect((ip, port))
        print("File Downloder Started")

    def run(self):
        try:
            self.conn.send(self.hash.encode('utf-8'))
            self.data_size = struct.unpack('>I', self.conn.recv(4))[0]
            filename = str(self.conn.recv(4096).decode('utf-8')) #recieve file name
            received_payload = b""
            reamining_payload_size = data_size
            while reamining_payload_size != 0:
                received_payload += self.conn.recv(reamining_payload_size)
                reamining_payload_size = self.data_size - len(received_payload)
            data = pickle.loads(received_payload)

            self.conn.close()

            f = open(filename, "w")
            f.write(data)
            f.close()
            dtrm.refresh()
            print("File Downloder Finished")

        except Exception as e:
            self.debug_print("File Downloader: Server errored or timed out.")
