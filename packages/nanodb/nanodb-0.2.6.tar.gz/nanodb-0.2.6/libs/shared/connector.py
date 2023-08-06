import zmq


class Connector(object):
    def __init__(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect("tcp://127.0.0.1:{0}".format(port))
        self.socket = socket

    def send_command(self, cmd_name, data):
        payload = {
            "cmd": cmd_name,
            "data": data
        }

        self.socket.send_json(payload)
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)

        if poller.poll(2*1000):
            ret = self.socket.recv_json()
        else:
            raise IOError("Request timeout")

        if ret.get('status') == "error":
            raise Exception(ret.get('error'))
        else:
            return ret.get('data')

    @property
    def is_connected(self):
        try:
            self.send_command("ping", None)
        except IOError:
            return False
        else:
            return True

    def list_cubes(self):
        return self.send_command("list", None)

    def get_information(self, cube_name):
        return self.send_command("info", {
            "cube": cube_name
        })

    def serialize(self, cube_name):
        return self.send_command("serialize", {
            "cube": cube_name
        })

    def create_cube(self, input_file, config_file):
        return self.send_command("create", {
            "input": input_file,
            "config": config_file
        })

    def load_cube(self, nano_file):
        return self.send_command("load", {
            "file": nano_file
        })

    def drop(self, cube_name):
        return self.send_command("drop", {
            "cube": cube_name
        })

    def close_connection(self):
        self.socket.close()
