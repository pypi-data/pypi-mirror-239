import signal
import sys

from heisskleber.config import load_config
from heisskleber.network.zmq.config import ZMQConf
from heisskleber.network.zmq.subscriber import ZMQRawSubscriber
from heisskleber.rawlogger.config import RawLoggerConf
from heisskleber.rawlogger.rawlogger import RawLogger


def signal_handler(sig, frame):
    print("msb_rawlogger.py exit")

    sys.exit(0)


class RawLoggerService:
    def __init__(self, config: RawLoggerConf, subscriber: ZMQRawSubscriber):
        self.excluded_topics = set(config.excluded_topics)
        self.config = config
        self.subscriber = subscriber
        self.logger = RawLogger(config)
        if self.config.verbose:
            print(self.config)

    def get_data(self) -> tuple[bytes, bytes]:
        while True:
            try:
                (topic, data) = self.subscriber.receive()
            except Exception as e:  # TODO specify exception subclass
                print(f"failed to receive message: {e}")
                continue
            yield topic, data

    def run(self):
        for topic, data_raw in self.get_data():
            topic_decoded = topic.decode("utf-8")
            if topic_decoded not in self.excluded_topics:
                if self.config.print_stdout:
                    print(f"{topic_decoded} : {data_raw.decode('utf-8')}")

                data = b'{"' + topic + b'":' + data_raw + b"}\n"
                self.logger.write(data)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    raw_logger_config = load_config(RawLoggerConf(), "rawlogger")
    zmq_config = load_config(ZMQConf(), "zmq")
    subscriber = ZMQRawSubscriber(raw_logger_config.included_topics, zmq_config)
    raw_logger_service = RawLoggerService(raw_logger_config, subscriber)
    raw_logger_service.run()
