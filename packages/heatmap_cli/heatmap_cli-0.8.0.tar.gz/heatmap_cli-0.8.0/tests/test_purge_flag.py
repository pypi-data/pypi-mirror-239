# pylint: disable=C0114,C0116

import pytest


@pytest.mark.parametrize("option", ["-p", "--purge"])
def test_debug_logs(cli_runner, csv_file, option):
    csv = csv_file("sample.csv")
    ret = cli_runner(csv, "-d", option)
    assert "purge=True" in ret.stderr


def test_purge_output_folder_if_exists(cli_runner, csv_file):
    csv = csv_file("sample.csv")
    output_folder = csv.resolve().parent.joinpath("output")
    output_folder.mkdir(parents=True, exist_ok=True)
    ret = cli_runner(csv, "-d", "-p")
    assert f"Purge output folder: {output_folder}" in ret.stderr
