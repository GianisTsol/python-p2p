import threading
import socket
import pickle
from . import data_request_management as dtrm
import time
import struct


class fileClientThread(threading.Thread):
    def __init__(self, ip, port, conn, file_requested):
        super(fileClientThread, self).__init__()  # CAll Thread.__init__()
        self.terminate_flag = threading.Event()
        self.ip = ip
        self.port = port
        self.sock = conn
        self.file_requested = file_requested

    def SendFile(self, filehash):
        content = dtrm.getallfiles()
        filehash = str(filehash)
        if not dtrm.have_file(filehash):
            print("File requested to download but we do not have: " + filehash)
            self.sock.close()
        else:
            file = content[filehash]["name"]
            filep = content[filehash]["path"]
            with open(filep, "rb") as f:
                data = f.read()
            serialized_data = pickle.dumps(data)
            self.sock.sendall(struct.pack(">I", len(serialized_data)))
            time.sleep(0.1)
            print("File: " + file)
            self.sock.send(file.encode("utf-8"))
            time.sleep(0.1)
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
        super(fileServer, self).__init__()  # CAll Thread.__init__()

        self.parent = parent
        self.port = PORT

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(10.0)
        self.sock.bind(("", self.port))
        self.sock.listen(1)

        self.threads = []

        self.dirname = ""

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        print("File Server Started")
        while (
            not self.terminate_flag.is_set()
        ):  # Check whether the thread needs to be closed
            try:
                (conn, (ip, port)) = self.sock.accept()

                self.parent.debug_print("File Server conection from: " + str(ip))

                file_requested = str(
                    conn.recv(4096).decode("utf-8")
                )  # recieve file hash
                print("Sending file: " + file_requested)
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
    def __init__(self, ip, port, fhash, dirname):
        super(FileDownloader, self).__init__()
        self.terminate_flag = threading.Event()
        self.fhash = str(fhash)
        self.dirnamme = dirname
        self.invalid_chars = ["/", "\\", "|", "*", "<", ">", ":", "?", '"']
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(10.0)
        self.conn.connect((ip, port))
        print("File Downloder Started")

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        try:
            self.conn.send(self.fhash.encode("utf-8"))
            self.data_size = struct.unpack(">I", self.conn.recv(9))[0]
            time.sleep(0.1)
            print("file size: " + str(self.data_size))
            self.filename = str(
                self.conn.recv(256).decode("utf-8")
            )  # recieve file name
            print("file name:" + str(self.filename))
            for i in self.invalid_chars:
                if i in self.filename:
                    print("INVALID FILE NAME. ABORTING.")
                    self.stop()
                    return
            time.sleep(0.1)
            received_payload = b""
            reamining_payload_size = self.data_size
            while reamining_payload_size != 0 and not self.terminate_flag.is_set():
                received_payload += self.conn.recv(reamining_payload_size)
                reamining_payload_size = self.data_size - len(received_payload)
            data = pickle.loads(received_payload)

            self.conn.close()

            with open(self.dirnamme + self.filename, "wb") as f:
                f.write(data)
            if not dtrm.hash_data(self.dirnamme + self.filename) == self.fhash:
                print("Recieved corrupt file, deleting....")
            self.finished = True
            print("File Downlod Finished")
            dtrm.addfile(self.dirnamme + self.filename)

        except Exception as e:
            print("File Downloader: Server errored or timed out.")
            # raise(e)
            self.stop()
