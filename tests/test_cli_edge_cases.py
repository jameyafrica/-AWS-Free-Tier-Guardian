import pytest
from unittest.mock import patch
from botocore.exceptions import ClientError, NoCredentialsError
import main as main_module


def test_no_credentials_error_exits_nonzero(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py"])
    with patch("main.get_running_instances", side_effect=NoCredentialsError()):
        with pytest.raises(SystemExit) as exc_info:
            main_module.main()
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "AWS credentials not found" in captured.out


def test_access_denied_exits_nonzero(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py"])
    error_response = {"Error": {"Code": "AccessDenied", "Message": "denied"}}
    with patch("main.get_running_instances", side_effect=ClientError(error_response, "DescribeInstances")):
        with pytest.raises(SystemExit) as exc_info:
            main_module.main()
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "IAM policy" in captured.out
