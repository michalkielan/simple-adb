#
# file utils.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

"""Utils"""
import re

IP_ADDRESS_REGEX = (
    r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
)


def is_valid_ip(address):
    """Check for valid ip address using regex

       Args:
         address (str): Ip address
    """
    try:
        ip_valid = re.match(IP_ADDRESS_REGEX, address)
        return bool(ip_valid)
    except TypeError:
        return False
