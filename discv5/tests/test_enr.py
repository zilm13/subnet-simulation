import pytest

from enr import ENR


@pytest.mark.parametrize(
    "ip,port,id_hex,expected",
    (
            ("127.0.0.1", 30303,
             "0000000000000000000000000000000000000000000000000000000000000001", "127.0.0.1"),
    )
)
def test_enr(ip, port, id_hex, expected):
    """
    Just testing the way we are working with NamedTuple inherited structures
    """
    enr1 = ENR.from_values(ip, port, bytes.fromhex(id_hex))
    assert enr1.ip == expected
