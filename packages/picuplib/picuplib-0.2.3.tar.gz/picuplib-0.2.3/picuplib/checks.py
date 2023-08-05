# -*- coding:utf8 -*-
######################## BEGIN LICENSE BLOCK ########################
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
######################### END LICENSE BLOCK #########################
"""
module for some argument cheking
"""

from json import loads

from picuplib.exceptions import (UnsuportedResize, UnsuportedRotation,
                                 UnsupportedFormat, UnkownError)
from picuplib.globals import ALLOWED_ROTATION, ALLOWED_RESIZE


def check_rotation(rotation):
    """checks rotation parameter if illegal value raises exception"""

    if rotation not in ALLOWED_ROTATION:
        allowed_rotation = ', '.join(ALLOWED_ROTATION)
        raise UnsuportedRotation('Rotation %s is not allwoed. Allowed are %s'
                                 % (rotation, allowed_rotation))

def check_resize(resize):
    """checks resize parameter if illegal value raises exception"""

    if resize not in ALLOWED_RESIZE:
        allowed_resize = ', '.join(ALLOWED_RESIZE)
        raise UnsuportedResize('Resize %s is not allowed. Allowed are %s'
                               % (resize, allowed_resize))

def check_noexif(noexif):
    """checks if noexif parameter is boolean"""
    if not isinstance(noexif, bool):
        raise TypeError('noexif must be boolean')

def check_response(response):
    """
    checks the response if the server returned an error raises an exception.
    """
    response = response.replace('null', '')
    response = loads(response)
    if 'failure' in response:
        if response['failure'] == 'Falscher Dateityp':
            raise UnsupportedFormat('Please look at picflash.org '
                                    'witch formats are supported')
        else:
            raise UnkownError(response['failure'])
