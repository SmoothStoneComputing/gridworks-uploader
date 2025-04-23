"""Local pytest configuration"""

from pathlib import Path

import pytest
from gwproactor_test import (  # noqa: F401
    default_test_env,
    restore_loggers,
)
from gwproactor_test.certs import set_test_certificate_cache_dir
from gwproactor_test.pytest_options import add_live_test_options

set_test_certificate_cache_dir(Path(__file__).parent / ".certificate_cache")


def pytest_addoption(parser: pytest.Parser) -> None:
    add_live_test_options(parser)
