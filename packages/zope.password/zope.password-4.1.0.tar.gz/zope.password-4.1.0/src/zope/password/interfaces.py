##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Password manager interface
"""
import zope.interface

class IPasswordManager(zope.interface.Interface):
    """Password manager"""

    def encodePassword(password):
        """Return encoded data for the given password

        The encoded password is a bytes string.
        """

    def checkPassword(encoded_password, password):
        """Does the given encoded data coincide with the given password
        """

class IMatchingPasswordManager(IPasswordManager):
    """Password manager with hash matching support"""

    def match(encoded_password):
        """
        Returns True when the given data was encoded with the scheme
        implemented by this password manager.

        """
