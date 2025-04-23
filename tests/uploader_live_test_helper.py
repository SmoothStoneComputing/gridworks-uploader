import logging
from typing import Any

from gwproactor_test import LiveTest

from gwupload import UploaderApp
from gwupload.app import UploaderSettings
from gwupload.stubs.ingester.ingester import StubIngesterApp, StubIngesterSettings
from gwupload.stubs.names import STUB_INGESTER_LONG_NAME


class UploaderLiveTest(LiveTest):
    UPLOADER_LONG_NAME = "test_uploader"

    @classmethod
    def child_app_type(cls) -> type[UploaderApp]:
        return UploaderApp

    @classmethod
    def parent_app_type(cls) -> type[StubIngesterApp]:
        return StubIngesterApp

    def __init__(self, **kwargs: Any) -> None:
        kwargs["child_app_settings"] = kwargs.get(
            "child_app_settings",
            UploaderSettings(
                long_name=self.UPLOADER_LONG_NAME,
                ingester_long_name=STUB_INGESTER_LONG_NAME,
            ),
        )
        kwargs["parent_app_settings"] = kwargs.get(
            "parent_app_settings",
            StubIngesterSettings(
                uploader_long_name=self.UPLOADER_LONG_NAME,
                event_logger_level=logging.INFO,
            ),
        )
        super().__init__(**kwargs)
