# !/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 trgk

# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#    3. This notice may not be removed or altered from any source
#    distribution.
#
# See eudtrg.LICENSE for more info


'''
String table manager. Internally used in eudtrg.
'''

 

from . import binio, ubconv


class TBL:

    def __init__(self, content=None):
        #
        # datatb : table of strings                      : string data table
        # dataindextb : string id -> data id             : string offset table
        # stringmap : string -> representative string id
        #

        self._datatb = []
        self._stringmap = {}
        self._dataindextb = []  # String starts from #1
        self._capacity = 2  # Size of STR section

        if content is not None:
            self.LoadData(content)

    def LoadData(self, content):
        self._datatb.clear()
        self._stringmap.clear()
        self._capacity = 2

        stringcount = binio.b2i2(content, 0)
        for i in range(stringcount):
            i += 1
            stringoffset = binio.b2i2(content, i * 2)
            send = stringoffset
            while content[send] != 0:
                send += 1

            string = content[stringoffset:send]
            self.AddString(string)

    def AddString(self, string):
        if type(string) is str:
            string = ubconv.u2b(string)  # Starcraft uses multibyte encoding.

        stringindex = len(self._dataindextb)

        # If duplicate text exist -> just proxy it
        try:
            repr_stringid = self._stringmap[string]
            dataindex = self._dataindextb[repr_stringid]
            self._dataindextb.append(dataindex)
            self._capacity += 2  # just string offset

        # Else -> Create new entry
        except KeyError:
            dataindex = len(self._datatb)
            self._stringmap[string] = stringindex
            self._datatb.append(string)
            self._dataindextb.append(dataindex)
            # string + b'\0' + string offset
            self._capacity += len(string) + 1 + 2

        assert self._capacity < 65536, 'String table overflow'

        return stringindex

    def GetString(self, index):
        if index == 0:
            return None
        else:
            try:
                return self._datatb[index - 1]
            except IndexError:
                return None

    def GetStringIndex(self, string):
        try:
            return self._stringmap[string] + 1

        except KeyError:
            return self.AddString(string) + 1

    def SaveTBL(self):
        outbytes = []

        # calculate offset of each string
        stroffset = []
        outindex = 2 * len(self._dataindextb) + 2
        for s in self._datatb:
            stroffset.append(outindex)
            outindex += len(s) + 1

        # String count
        outbytes.append(binio.i2b2(len(self._dataindextb)))

        # String offsets
        for dataidx in self._dataindextb:
            outbytes.append(binio.i2b2(stroffset[dataidx]))

        # String data
        for s in self._datatb:
            outbytes.append(s)
            outbytes.append(b'\0')

        return b''.join(outbytes)
