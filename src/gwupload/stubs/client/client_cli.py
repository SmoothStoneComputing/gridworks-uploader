import httpx
import rich
import typer

from gwupload.stubs.client.client import upload_packet

app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    rich_markup_mode="rich",
    help="Stub client for Gridworks Uploader",
)


@app.command()
def run(
    *,
    num_packets: int = 1,
    readings_per_packet: int = 2,
    sensor_name: str = "dark-massometer",
    unit: str = "kg",
) -> None:
    """Generate and upload random data to local Gridworks Uploader"""

    for packet_idx in range(num_packets):
        response = upload_packet(
            readings_per_packet=readings_per_packet,
            sensor_name=sensor_name,
            unit=unit,
        )
        rich.print(f"Packet {packet_idx + 1} / {num_packets}")
        # noinspection PyProtectedMember
        httpx._main.print_response(response)  # noqa: SLF001


@app.callback()
def _main() -> None: ...


if __name__ == "__main__":
    app()
