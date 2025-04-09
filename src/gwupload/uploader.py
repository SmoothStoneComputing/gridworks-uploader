import typing

from gwproactor import CodecFactory, PrimeActor, ServicesInterface
from gwproactor.message import MQTTReceiptPayload
from gwproto import Message
from gwproto.messages import EventBase


class UploaderCodecFactory(CodecFactory): ...


class Uploader(PrimeActor):
    INGESTER_LINK: str = "ingester"
    LISTENER_LINK: str = "listener"

    def __init__(self, name: str, services: ServicesInterface) -> None:
        super().__init__(name, services)

    @classmethod
    def get_codec_factory(cls) -> UploaderCodecFactory:
        return UploaderCodecFactory()

    def process_internal_message(self, message: Message[typing.Any]) -> None:
        self.services.logger.path(
            f"++{self.name}._derived_process_message "
            f"{message.Header.Src}/{message.Header.MessageType}"
        )
        path_dbg = 0
        match message.Payload:
            case _:
                path_dbg |= 0x00000001
        self.services.logger.path(
            "--{self.name}._derived_process_message  path:0x{path_dbg:08X}"
        )

    def process_mqtt_message(
        self,
        message: Message[MQTTReceiptPayload],
        decoded: Message[typing.Any],
    ) -> None:
        self.services.logger.path(
            f"++{self.name}._derived_process_mqtt_message {message.Payload.message.topic}",
        )
        path_dbg = 0
        if message.Payload.client_name == self.LISTENER_LINK:
            path_dbg |= 0x00000001
            self._process_listener_mqtt_message(message, decoded)
        self.services.logger.path(
            f"--{self.name}._derived_process_mqtt_message  path:0x{path_dbg:08X}",
        )

    def _process_listener_mqtt_message(
        self, message: Message[MQTTReceiptPayload], decoded: Message[typing.Any]
    ) -> None:
        self.services.logger.path(
            f"++{self.name}._process_listener_mqtt_message {message.Payload.message.topic}",
        )
        path_dbg = 0
        match decoded.Payload:
            case EventBase():
                path_dbg |= 0x00000001
                self.services.generate_event(decoded.Payload)
            case _:
                path_dbg |= 0x00000002
        self.services.logger.path(
            f"--{self.name}._process_listener_mqtt_message  path:0x{path_dbg:08X}",
        )
