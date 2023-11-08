import os

from heisskleber.config import load_config
from heisskleber.network.mqtt import MQTTConf, MqttPublisher, MqttSubscriber
from heisskleber.network.serial import SerialConf, SerialPublisher, SerialSubscriber
from heisskleber.network.zmq import ZMQConf, ZmqPublisher, ZmqSubscriber

from .types import Publisher, Subscriber

_registered_publishers = {}
_registered_subscribers = {}


def get_publisher(name: str):
    if name not in _registered_publishers:
        raise KeyError(f"{name} is not a registered Publisher.")

    pub_cls, conf_cls = _registered_publishers[name]

    if "MSB_CONFIG_DIR" in os.environ:
        print(f"loading {name} config")
        config = load_config(conf_cls(), name, read_commandline=False)
    else:
        print(f"using default {name} config")
        config = conf_cls()

    return pub_cls(config)


def get_subscriber(name: str, topic):
    if name not in _registered_publishers:
        raise KeyError(f"{name} is not a registered Subscriber.")

    sub_cls, conf_cls = _registered_subscribers[name]

    if "MSB_CONFIG_DIR" in os.environ:
        print(f"loading {name} config")
        config = load_config(conf_cls(), name, read_commandline=False)
    else:
        print(f"using default {name} config")
        config = conf_cls()

    return sub_cls(topic, config)


def register_publisher(name, publisher_class: Publisher, config):
    _registered_publishers[name] = (publisher_class, config)


def register_subscriber(name, subscriber_class: Subscriber, config):
    _registered_subscribers[name] = (subscriber_class, config)


register_publisher("zmq", ZmqPublisher, ZMQConf)
register_publisher("mqtt", MqttPublisher, MQTTConf)
register_publisher("serial", SerialPublisher, SerialConf)

register_subscriber("zmq", ZmqSubscriber, ZMQConf)
register_subscriber("mqtt", MqttSubscriber, MQTTConf)
register_subscriber("serial", SerialSubscriber, SerialConf)
