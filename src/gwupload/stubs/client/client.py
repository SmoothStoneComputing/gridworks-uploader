import random
import time
from typing import Literal, Self

import httpx
from gwproto.messages import EventBase
from httpx import Response
from pydantic import model_validator


class SomeData(EventBase):
    TimestampsUTC: list[float]
    Readings: list[float]
    SensorName: str = ""
    Unit: str = ""
    TypeName: Literal["gridworks.event.some.data"] = "gridworks.event.some.data"

    @model_validator(mode="after")
    def validate_lengths(self) -> Self:
        if len(self.TimestampsUTC) != len(self.Readings):
            raise ValueError(
                f"ERROR. Got {len(self.TimestampsUTC)} timestamps "
                f"but {len(self.Readings)} readings."
            )
        return self


def generate_data(
    readings_per_packet: int = 3,
    sensor_name: str = "dark-massometer",
    unit: str = "kg",
) -> SomeData:
    now = time.time()
    return SomeData(
        TimestampsUTC=[
            now - (reading + 1) * 5 for reading in range(readings_per_packet)
        ],
        Readings=[random.random() for _ in range(readings_per_packet)],  # noqa: S311
        SensorName=sensor_name,
        Unit=unit,
    )


def upload_packet(
    readings_per_packet: int = 3,
    sensor_name: str = "dark-massometer",
    unit: str = "kg",
) -> Response:
    data = generate_data(
        readings_per_packet=readings_per_packet, sensor_name=sensor_name, unit=unit
    )
    return httpx.post("http://127.0.0.1:8080/events", json=data.model_dump())


if __name__ == "__main__":
    upload_packet()
