import pytest

from util import (log_distance, log_distance_sim)


@pytest.mark.parametrize(
    "id1_hex,id2_hex,expected_distance",
    (
            ("0000000000000000000000000000000000000000000000000000000000000001",
             "0000000000000000000000000000000000000000000000000000000000000001", 0),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "0000000000000000000000000000000000000000000000000000000000000001", 1),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "1000000000000000000000000000000000000000000000000000000000000000", 253),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "1111111111111111111111111111111111111111111111111111111111111111", 253),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "9999999999999999999999999999999999999999999999999999999999999999", 256),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 256),
            ("9999999999999999999999999999999999999999999999999999999999999999",
             "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 255),
    )
)
def test_log_distance(id1_hex, id2_hex, expected_distance):
    id1 = bytes.fromhex(id1_hex)
    id2 = bytes.fromhex(id2_hex)
    assert log_distance(id1, id2) == expected_distance


@pytest.mark.parametrize(
    "id1_hex,id2_hex,expected_distance",
    (
            ("0000000000000000000000000000000000000000000000000000000000000001",
             "0000000000000000000000000000000000000000000000000000000000000001", 0),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "0000000000000000000000000000000000000000000000000000000000000001", 1),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "1000000000000000000000000000000000000000000000000000000000000000", 32),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "1111111111111111111111111111111111111111111111111111111111111111", 32),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "9999999999999999999999999999999999999999999999999999999999999999", 32),
            ("0000000000000000000000000000000000000000000000000000000000000000",
             "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 32),
            ("9999999999999999999999999999999999999999999999999999999999999999",
             "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 32),
    )
)
def test_log_distance_sim(id1_hex, id2_hex, expected_distance):
    id1 = bytes.fromhex(id1_hex)
    id2 = bytes.fromhex(id2_hex)
    assert log_distance_sim(id1, id2) == expected_distance
