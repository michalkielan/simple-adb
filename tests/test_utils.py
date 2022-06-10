#
# file test_utils.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

"""Unit tests for adb commands"""
import pytest
import simpleadb


@pytest.mark.parametrize(
    "address,expected",
    [
        ("127.0.0.1", True),
        ("192.168.0.1", True),
        ("0.0.0.0", True),
        ("localhost", False),
        ("192.169.256", False),
        ("0", False),
        ("1.1.1.", False),
        (42, False),
    ],
)
def test_ip_match(address, expected):
    """Test for a valid ip"""
    assert simpleadb.utils.is_valid_ip(address) == expected
