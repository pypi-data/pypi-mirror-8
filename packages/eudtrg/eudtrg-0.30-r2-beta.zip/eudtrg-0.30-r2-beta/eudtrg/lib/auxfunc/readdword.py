 #!/usr/bin/python
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


from eudtrg.base import *  # @UnusedWildImport
from eudtrg.lib.baselib import *  # @UnusedWildImport


@EUDFunc
def f_dwread_epd(targetplayer):
    '''
    Read dword from memory. This function can read any memory with read access.
    :param targetplayer: EPD Player for address to read.
    :returns: Memory content.
    '''
    ret = EUDCreateVariables(1)

    # Common comparison trigger
    PushTriggerScope()
    cmp = Forward()
    cmp_player = cmp + 4
    cmp_number = cmp + 8
    cmpact = Forward()

    cmptrigger = Forward()
    cmptrigger << Trigger(
        conditions=[
            cmp << Memory(0, AtMost, 0)
        ],
        actions=[
            cmpact << SetMemory(cmptrigger + 4, SetTo, 0)
        ]
    )
    cmpact_ontrueaddr = cmpact + 20
    PopTriggerScope()

    # static_for
    chain1 = [Forward() for _ in range(32)]
    chain2 = [Forward() for _ in range(32)]

    # Main logic start
    SeqCompute([
        (EPD(cmp_player), SetTo, targetplayer),
        (EPD(cmp_number), SetTo, 0xFFFFFFFF),
        (ret,             SetTo, 0xFFFFFFFF)
    ])

    readend = Forward()

    for i in range(31, -1, -1):
        nextchain = chain1[i - 1] if i > 0 else readend

        chain1[i] << Trigger(
            nextptr=cmptrigger,
            actions=[
                SetMemory(cmp_number, Subtract, 2 ** i),
                ret.SubtractNumber(2 ** i),
                SetNextPtr(cmptrigger, chain2[i]),
                SetMemory(cmpact_ontrueaddr, SetTo, nextchain)
            ]
        )

        chain2[i] << Trigger(
            actions=[
                SetMemory(cmp_number, Add, 2 ** i),
                ret.AddNumber(2 ** i)
            ]
        )

    readend << NextTrigger()

    return ret
