# pylint: disable=line-too-long
#
# file utils.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

"""Module contains utility functions"""
import re

IP_ADDRESS_REGEX = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


def is_valid_ip(address: str) -> bool:
    """Check for valid ip address using regex.

    :param str address: Package name.
    :return: True is address is a valid IP address, False otherwise.
    :rtype: bool

    :example:

    >> is_valid_ip('192.168.42.42')
    True
    >> is_valid_ip('localhost')
    False
    """
    try:
        ip_valid = re.match(IP_ADDRESS_REGEX, address)
        return bool(ip_valid)
    except TypeError:
        return False
