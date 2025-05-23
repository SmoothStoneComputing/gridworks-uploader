# Gridworks Uploader

[![PyPI](https://img.shields.io/pypi/v/gridworks-uploader.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/gridworks-uploader.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/gridworks-uploader)][python version]
[![License](https://img.shields.io/pypi/l/gridworks-uploader)][license]

[![Read the documentation at https://gridworks-uploader.readthedocs.io/](https://img.shields.io/readthedocs/gridworks-uploader/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/SmoothStoneComputing/gridworks-uploader/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/SmoothStoneComputing/gridworks-uploader/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]

[pypi_]: https://pypi.org/project/gridworks-uploader/
[status]: https://pypi.org/project/gridworks-uploader/
[python version]: https://pypi.org/project/gridworks-uploader
[read the docs]: https://gridworks-uploader.readthedocs.io/
[tests]: https://github.com/SmoothStoneComputing/gridworks-uploader/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/anschweitzer/gridworks-uploader
[pre-commit]: https://github.com/pre-commit/pre-commit

This package provides a reliable upload service using the [gridworks-protocol]. 

The upload services communicates upstream using MQTT. Clients deliver data to
the service for reliable delivery using http. For [example]: 

```python
    import random
    import time
    from typing import Literal
    
    import httpx
    from gwproto.messages import EventBase
    
    
    class SomeData(EventBase):
        TimestampUTC: float
        Reading: float
        TypeName: Literal["gridworks.event.some.data"] = "gridworks.event.some.data"
    
    
    if __name__ == "__main__":
        httpx.post(
            "http://127.0.0.1:8080/events",
            json=SomeData(
                TimestampUTC=round(time.time(), 3),
                Reading=round(random.random(), 3),
            ).model_dump(),
        )
```

## Experimentation

To experiment with this package you must run the upload service, and, if you
want to watch your messages delivered to a stub ingester, you must also run an
MQTT broker and the stub ingester. 

To set up the MQTT broker, follow the [gridworks-proactor instructions].

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
uv tool install -p 3.12 poetry=1.8.5
git clone https://github.com/SmoothStoneComputing/gridworks-uploader.git
cd gridworks-uploader
```
Create a `.env` file at the location returned by: 
```shell
gwup envfile
```

with these contents:
```
UPLOADER_APP_lONG_NAME = "test.uploader"
UPLOADER_APP_INGESTER_LONG_NAME = "test.ingester"
STUB_INGESTER_APP_lONG_NAME = "test.ingester"
STUB_INGESTER_APP_UPLOADER_LONG_NAME = "test.uploader"
```

Create local test certificate authority:
```shell
poetry install --sync --with dev
poetry shell
gwcert ca create test-ca
```

Generate test certs for the uploader and the stub ingester:
```shell
gwup gen-test-certs
gwup stubs ingester gen-test-certs
```

Open 3 terminals. In each terminal, cd to the gridworks-uploader repo and run:
```shell
poetry shell
```

In the ingester terminal run:
```shell
gwup stubs ingester run --log-events
```

In the uploader terminal run:
```shell 
gwup run --message-summary
```

In the client terminal run:
```shell
gwup stubs client run 
```

Or:
```shell
python src/gwupload/stubs/client/client.py 
```


## Installation

You can install _Gridworks Uploader_ via [pip] from [PyPI]:

```shell
uv tool install gridworks-uploader
```
or
```
pipx install gridworks-uploader
```

## Service installation
Gridworks-Uploader can be installed as a [systemd] service,
for example on a Raspberry Pi, using `gwup service` command line interface. 
The gwup service commands are mostly wrappers around [systemctl] and [journalctl].
To see the systemctl and journalctl command without running them simply pass
`--dry-run` to any gwup service command.

### Unit file generation

The configuration for the service is stored in a [unit file]. To generate a
service file run:

```shell
gwup service generate
```
or, if the service will not run under default user, 'pi', but the user USER_NAME, 
run: 
```shell
gwup service generate --user USER_NAME
```

The unit file can be also be written or edited by hand. The service file is
generated at `$HOME/.config/gridworks/uploader/gridworks-uploader.service`.
That path can be viewed any time with: 
```shell
gwup service file
```

Once the service is installed changes to the unit file will not take effect
unless the unit file is reloaded into systemd with `sudo systemctl daemon-reload`
and the service is restarted. This can be accomplished with: 
```shell
gwup service reload
gwup service restart
```

### Installation
To install and run the service run:
```shell
gwup service install
```

To stop and uninstall the service run:
```shell
gwup service uninstall
```
The service can be re-installed without re-generating the unit file. 

### Starting and stopping

The service can be started, restarted and stopped: 
```shell
gwup service start
```
```shell
gwup service restart
```

```shell
gwup service stop
```
A stopped service will restart when the device reboots. Use `gwup service uninstall`
to prevent the service from restarting when the device reboots. 

### Watching
The current state of the service can be seen with:
```shell
gwup service status
```
The log of the service can be followed with: 
```shell
gwup service log
```


## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Gridworks Uploader_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/SmoothStoneComputing/gridworks-uploader/issues
[pip]: https://pip.pypa.io/
[example]: https://github.com/SmoothStoneComputing/gridworks-uploader/blob/dev/src/gwupload/stubs/client/client.py
[gridworks-protocol]: https://github.com/thegridelectric/gridworks-protocol
[gridworks-proactor instructions]: https://github.com/SmoothStoneComputing/gridworks-proactor/tree/2.X/has-a?tab=readme-ov-file#requirements
[systemd]: https://www.man7.org/linux/man-pages/man1/systemd.1.html
[unit file]: https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#
[systemctl]: https://www.man7.org/linux/man-pages/man1/systemctl.1.html
[journalctl]: https://www.man7.org/linux/man-pages/man1/journalctl.1.html

<!-- github-only -->

[license]: https://github.com/SmoothStoneComputing/gridworks-uploader/blob/dev/LICENSE
[contributor guide]: https://github.com/SmoothStoneComputing/gridworks-uploader/blob/main/CONTRIBUTING.md
[command-line reference]: https://gridworks-uploader.readthedocs.io/en/latest/usage.html


