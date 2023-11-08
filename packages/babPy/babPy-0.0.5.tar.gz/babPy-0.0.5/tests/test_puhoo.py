import pytest
from  babpy.talk import puhoo


def test_puhoo_string(capsys):
    puhoo("Hello, World!")
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"

def test_puhoo_number(capsys):
    puhoo(1)
    captured = capsys.readouterr()
    assert captured.out == "1\n"

def test_puhoo_object(capsys):
    puhoo({"a":"b"})
    captured = capsys.readouterr()
    assert captured.out == "{'a': 'b'}\n"


if __name__ == "__main__":
    pytest.main()
