from pathlib import Path
from typing import Any, Optional

from gwproactor import App, LinkSettings, ProactorName, ProactorSettings
from gwproactor.config import MQTTClient
from gwproactor.persister import TimedRollingFilePersister
from gwproto import HardwareLayout
from pydantic_settings import BaseSettings

from gwupload.uploader import Uploader


class UploaderSettings(BaseSettings):
    paths_name: str = ""
    ingester_long_name: str = ""
    ingester_short_name: str = ""


class UploaderApp(App):
    INGESTER_LINK: str = Uploader.INGESTER_LINK
    LISTENER_LINK: str = Uploader.LISTENER_LINK
    UPLOAD_SRC_LONG_NAME: str = "upload_src"
    UPLOAD_SRC_SHORT_NAME: str = "usrc"

    app_settings: UploaderSettings

    def __init__(
        self,
        app_settings: Optional[UploaderSettings] = None,
        env_file: Optional[str | Path] = None,
        **kwargs: Any,
    ) -> None:
        self.app_settings = (
            UploaderSettings(_env_file=env_file)  # noqa
            if app_settings is None
            else app_settings
        )
        kwargs["paths_name"] = self.app_settings.paths_name
        kwargs["prime_actor_type"] = Uploader
        super().__init__(**kwargs)

    def _get_name(self, layout: HardwareLayout) -> ProactorName:
        return ProactorName(
            long_name=layout.scada_g_node_alias,
            short_name="s",
        )

    def _get_mqtt_broker_settings(
        self,
        name: ProactorName,  # noqa: ARG002
        layout: HardwareLayout,  # noqa: ARG002
    ) -> dict[str, MQTTClient]:
        return {
            link_name: MQTTClient()
            for link_name in [self.INGESTER_LINK, self.LISTENER_LINK]
        }

    def _get_link_settings(
        self,
        name: ProactorName,  # noqa: ARG002
        layout: HardwareLayout,
        brokers: dict[str, MQTTClient],  # noqa: ARG002
    ) -> dict[str, LinkSettings]:
        return {
            self.INGESTER_LINK: LinkSettings(
                broker_name=self.INGESTER_LINK,
                peer_long_name=layout.atn_g_node_alias,
                peer_short_name="i",
                upstream=True,
            ),
            self.LISTENER_LINK: LinkSettings(
                broker_name=self.LISTENER_LINK,
                peer_long_name=self.UPLOAD_SRC_LONG_NAME,
                peer_short_name=self.UPLOAD_SRC_SHORT_NAME,
                link_subscription_short_name=layout.scada_g_node_alias,
            ),
        }

    @classmethod
    def _make_persister(cls, settings: ProactorSettings) -> TimedRollingFilePersister:
        return TimedRollingFilePersister(settings.paths.event_dir)
