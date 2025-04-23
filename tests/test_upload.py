import time
from typing import Any

import httpx
import pytest
from gw_test import await_for
from gwproactor.logging_setup import enable_aiohttp_logging

from gwupload.stubs.client.client import SomeData
from tests.uploader_live_test_helper import UploaderLiveTest


@pytest.mark.asyncio
async def test_upload(request: Any) -> None:
    enable_aiohttp_logging()
    async with UploaderLiveTest(
        start_parent=True, start_child=True, request=request
    ) as t:
        linkU2I = t.child.links.link(t.child.upstream_client)
        statsI2U = t.parent.stats.link(t.parent.downstream_client)

        # wait for link to go active
        await await_for(
            linkU2I.active,
            1,
            "ERROR waiting for uploader to connect to ingester",
            err_str_f=t.summary_str,
        )
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                "http://127.0.0.1:8080/events",
                json=SomeData(
                    TimestampUTC=round(time.time(), 3),
                    Reading=38.00,
                ).model_dump(),
            )
        assert response.is_success, response.text
        await await_for(
            lambda: statsI2U.num_received_by_type["gridworks.event.some.data"] == 1,
            1,
            "ERROR waiting for ingester to receive event from uploader",
            err_str_f=t.summary_str,
        )
