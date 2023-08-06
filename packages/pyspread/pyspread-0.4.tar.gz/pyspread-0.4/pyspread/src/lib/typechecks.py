#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Martin Manns
# Distributed under the terms of the GNU General Public License

# --------------------------------------------------------------------
# pyspread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyspread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyspread.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

"""

Typechecks
==========

typechecks.py contains functions for checking type likeness,
i. e. existence of typical attributes of a type for objects.

"""


def is_slice_like(obj):
    """Returns True if obj is slice like, i.e. has attribute indices"""

    return hasattr(obj, "indices")


def is_string_like(obj):
    """Returns True if obj is string like, i.e. has method split"""

    return hasattr(obj, "split")


def is_generator_like(obj):
    """Returns True if obj is string like, i.e. has method next"""

    return hasattr(obj, "next")