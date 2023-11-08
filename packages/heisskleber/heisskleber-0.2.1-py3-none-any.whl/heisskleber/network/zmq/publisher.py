import sys

import zmq

from heisskleber.config import load_config
from heisskleber.network.packer import get_packer
from heisskleber.network.pubsub.types import Publisher

from .config import ZMQConf


class ZmqPublisher(Publisher):
    def __init__(self, config: ZMQConf):
        self.config = config

        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.PUB)

        self.pack = get_packer(config.packstyle)
        self.connect()

    def connect(self):
        try:
            self.socket.connect(self.config.publisher_address)
        except Exception as e:
            print(f"failed to bind to zeromq socket: {e}")
            sys.exit(-1)

    def send(self, topic: bytes, data: dict):
        data = self.pack(data)
        self.socket.send_multipart([topic, data.encode("utf-8")])

    def __del__(self):
        self.socket.close()


def get_default_publisher() -> ZmqPublisher:
    import os

    if "MSB_CONFIG_DIR" in os.environ:
        print("loading zmq config")
        config = load_config(ZMQConf(), "zmq", read_commandline=False)
    else:
        print("using default zmq config")
        config = ZMQConf()
    return ZmqPublisher(config)
