import textwrap

from typer.testing import CliRunner

from gwupload.cli import cli_app

runner = CliRunner()


def test_cli_completes() -> None:
    """This test just verifies that clis can execute dry-runs and help without
    exception. It does not attempt to test content of execution."""

    command: list[str]
    for command in [
        [],
        ["run", "--dry-run"],
        ["config"],
        ["gen-test-certs", "--dry-run"],
        ["stubs"],
        ["stubs", "ingester"],
        ["stubs", "ingester", "run", "--dry-run"],
        ["stubs", "ingester", "gen-test-certs", "--dry-run"],
        ["stubs", "ingester", "config"],
        ["stubs", "client"],
        ["stubs", "client", "run", "--num-packets", "0"],
        ["service"],
        ["service", "file"],
        ["service", "generate", "--help"],
        ["service", "start", "--dry-run"],
        ["service", "restart", "--dry-run"],
        ["service", "stop", "--dry-run"],
        ["service", "status", "--dry-run"],
        ["service", "log", "--dry-run"],
        ["service", "reload", "--dry-run"],
        ["service", "install", "--dry-run"],
        ["service", "uninstall", "--dry-run"],
    ]:
        result = runner.invoke(cli_app, command)
        result_str = (
            f"exit code: {result.exit_code}\n"
            f"\t{result!s} from command\n"
            f"\t<gwup {' '.join(command)}> with output\n"
            f"{textwrap.indent(result.output, '        ')}"
        )
        assert result.exit_code == 0, result_str
