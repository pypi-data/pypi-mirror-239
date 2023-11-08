from __future__ import annotations

from paho.mqtt.client import Client as MQTTClient

import uuid

from typing import TYPE_CHECKING, Union, Literal

if TYPE_CHECKING:
    from paho.mqtt.client import MQTTMessage


Topic = tuple[str, Literal[0, 1, 2]]


TEST_TOPIC: Topic = ("topic", 0)


class Base:
    def __init__(
        self, host: str, port: int, username: str = None, password: str = None, keepalive: int = 60, userdata=None
    ):
        self._client: Union[MQTTClient, None] = None

        self._host: str = host
        self._port: int = port
        self._keepalive: int = keepalive

        self._username: str = username
        self._password: str = password

        self._is_connected: bool = False
        self._userdata = userdata

    def connect(self, client_id: str = None) -> None:
        """

        Connect to MQTT Broker

        Args:
            client_id (Optional[str]): MQTT Client ID. If not Provided client_id will use an uuid:

        Returns: None

        """

        if not self._is_connected:
            _client_id: str = client_id if client_id is not None else uuid.uuid4().hex
            self._client = MQTTClient(f"{_client_id}", userdata=self._userdata)
            self._map_callback()

            if self._username is not None and self._password is not None:
                self._client.username_pw_set(self._username, self._password)
            self._client.connect(self._host, self._port, keepalive=self._keepalive)

            self._is_connected = True

    def disconnect(self) -> None:
        """

        Disconnect from MQTT Broker

        Returns: None

        """
        if self._is_connected:
            self._client.disconnect()
            self._is_connected = False

    def _map_callback(self):
        pass


class MQTTSubscriber(Base):
    def __init__(
        self, host: str, port: int, username: str = None, password: str = None, keepalive: int = 60, userdata=None
    ):
        super().__init__(host, port, username=username, password=password, keepalive=keepalive, userdata=userdata)
        self._topics: list[Topic] = []

    def set_topics(self, *topics: Union[str, Topic]) -> None:
        for topic in topics:
            if isinstance(topic, str):
                self._topics.append((topic, 0))
            else:
                self._topics.append(topic)

    def on_connect(self, client: MQTTClient, userdata: any, flags: dict, rc: int):
        pass

    def on_disconnect(self, client: MQTTClient, userdata: any, flags: dict):
        pass

    def on_message(self, client: MQTTClient, userdata: any, msg: MQTTMessage):
        pass


class MQTTPublisher(MQTTSubscriber):
    def publish(self, topic: str, payload: Union[str, bytes, bytearray, int, float], qos: int = 0):
        self._client.publish(topic, payload, qos=qos)
