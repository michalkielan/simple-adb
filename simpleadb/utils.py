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

IPV4_REGEX = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
IPV6_REGEX = r"^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})$|(^([0-9a-fA-F]{1,4}:){1,7}:$)"


def is_valid_ip(address: str) -> bool:
    """Check for valid IP address using regex.

    :param str address: IP address.
    :return: True is address is a valid IP address, False otherwise.
    :rtype: bool

    :example:

    >> is_valid_ip('192.168.42.42')
    True
    >> is_valid_ip('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
    True
    >> is_valid_ip('localhost')
    False
    """
    try:
        ipv4_valid = re.match(IPV4_REGEX, address)
        ipv6_valid = re.match(IPV6_REGEX, address)
        return bool(ipv4_valid or ipv6_valid)
    except TypeError:
        return False
