#!/usr/bin/env python2
# coding=utf-8
#
# Copyright 2014 Sascha Schirra
#
# This file is part of Ropper.
#
# Ropper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ropper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import ropperapp.common.enum as enum
from ropperapp.common.utils import toHex

class Category(enum.Enum):
    _enum_ = 'STACK_PIVOTING LOAD_REG LOAD_MEM STACK_SHIFT SYSCALL JMP CALL WRITE_MEM INC_REG CLEAR_REG SUB_REG ADD_REG XCHG_REG NONE'



class GadgetType(enum.Enum):
    _enum_ = 'ROP JOP ALL'


class Gadget(object):

    def __init__(self, arch):
        super(Gadget, self).__init__()
        self.__arch = arch
        self.__lines = []
        self._gadget = ''
        self._vaddr = 0x0
        self.__category = None
        self.__imageBase = 0x0

    @property
    def lines(self):
        return self.__lines

    @property
    def imageBase(self):
        return self.__imageBase

    @imageBase.setter
    def imageBase(self, base):
        self.__imageBase = base

    @property
    def vaddr(self):
        return self._vaddr

    def append(self, address, inst):
        self.__lines.append((address, inst))
        self._gadget += inst + '\n'

    def match(self, filter):
        if not filter or len(filter) == 0:
            return True
        return bool(re.search(filter, self._gadget))

    def addressesContainsBytes(self, bytes):
        line =  self.__lines[0]
        for b in bytes:

            address = line[0] + self.__imageBase

            b = ord(b)
            for i in range(4):
                if (address & 0xff) == b:

                    return True
                address >>= 8



    def simpleInstructionString(self):
        toReturn = ''
        for line in self.__lines:
            toReturn += line[1] + '; '

        return toReturn[:-2]

    def simpleString(self):
        toReturn = '%s: ' % toHex(self.__lines[0][0] + self.__imageBase, self.__arch.addressLength)
        toReturn += self.simpleInstructionString()
        return toReturn

    @property
    def category(self):
        if not self.__category:
            line = self.__lines[0][1]
            for cat, regexs in self.__arch._categories.items():
                for regex in regexs[0]:
                    match = re.match(regex, line)
                    if match:
                        for invalid in regexs[1]:
                            for l in self.__lines[1:]:
                                if l[1].startswith(invalid):
                                    self.__category = (Category.NONE,)
                                    return self.__category
                        self.__category = (cat, len(self.__lines) -1 ,match.groupdict())
                        return self.__category
            self.__category = (Category.NONE,)

        return self.__category

    def __len__(self):
        return len(self.__lines)

    def __cmp__(self, other):
        if isinstance(other, self.__class__) and len(self) == len(other):
            return cmp(str(self),str(other))
        return -1

    def __str__(self):
        toReturn = 'Gadget: %s\n' % (self.__lines[0][0] + self.__imageBase)
        for line in self.__lines:
            toReturn += toHex(line[0] + self.__imageBase, self.__arch.addressLength) +': '+ line[1] + '\n'

        return toReturn
