# Rekall Memory Forensics
# Copyright 2014 Google Inc. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

"""This module implements profile indexing.

Rekall relies on accurate profiles for reliable analysis of memory artifacts. We
depend on selecting the correct profile from the profile repository, but
sometimes it's hard to determine the exact profile to use. The profile
repository has index files that are used to lookup the correct profile quickly,
based on a limited set of symbols and offsets that are known, or can be easily
detected, about the image.
"""

__author__ = (
    "Michael Cohen <scudette@google.com>",
    "Adam Sindelar <adamsh@google.com>",
)

import logging

from rekall import addrspace
from rekall import obj


class Index(obj.Profile):
    """A profile which contains an index to locate other profiles."""
    index = None
    base_offset = 0

    PERFECT_MATCH = 1.0
    GOOD_MATCH = 0.75

    def _SetupProfileFromData(self, data):
        super(Index, self)._SetupProfileFromData(data)
        self.index = data.get("$INDEX")

    def copy(self):
        result = super(Index, self).copy()
        result.index = self.index.copy()

        return result

    def _TestSymbols(self, address_space, offset, possible_values):
        """Match any of the possible_values at offset.

        Return True if there is a match.
        """
        for value in possible_values:
            value = value.decode("hex")
            data = address_space.read(offset, len(value))
            if value == data:
                return True

    def _TestProfile(self, address_space, image_base, profile, symbols):
        """Match _all_ the symbols against this data."""
        count_matched = 0
        for offset, possible_values in symbols:
            # The possible_values can be a single string which means there is
            # only one option. If it is a list, then any of the symbols may
            # match at this offset to be considered a match.
            if isinstance(possible_values, basestring):
                possible_values = [possible_values]

            if self._TestSymbols(
                    address_space=address_space,
                    offset=image_base + offset,
                    possible_values=possible_values):
                logging.debug(
                    "%s matched offset %#x+%#x=%#x",
                    profile, offset, image_base, offset+image_base)
                count_matched += 1

        if count_matched > 0:
            logging.debug(
                "%s matches %d/%d comparison points",
                profile, count_matched, len(symbols))

        return float(count_matched) / len(symbols)

    def IndexHits(self, image_base, address_space=None):
        if address_space == None:
            address_space = self.session.GetParameter("default_address_space")

        # Only preload the data we need to read, based on the known max offset.
        min_offset = self.metadata("MinOffset", 0) + image_base
        max_offset = self.metadata("MaxOffset", 5*1024*1024) + image_base

        # If min_offset is negative then the index is faulty, even though that
        # may not have been obvious at the time it was generated. Go ahead and
        # explode.
        if min_offset < 0:
            raise RuntimeError("Profile index points to a negative offset.")

        data = address_space.read(min_offset, max_offset - min_offset)

        address_space = addrspace.BufferAddressSpace(
            base_offset=min_offset,
            data=data,
            session=self.session)

        for profile, symbols in self.index.iteritems():
            match = self._TestProfile(
                address_space=address_space,
                image_base=image_base,
                profile=profile,
                symbols=symbols)

            yield match, profile

    def LookupIndex(self, image_base, address_space=None):
        partial_matches = []
        for match, profile in self.IndexHits(image_base, address_space):
            if match == self.PERFECT_MATCH:
                # Yield perfect matches right away.
                yield (profile, self.PERFECT_MATCH)

            elif match > 0:
                # Imperfect matches will be saved and returned in order of
                # accuracy.
                partial_matches.append((match, profile))

        partial_matches.sort(reverse=True)
        for match, profile in partial_matches:
            yield (profile, match)

