from __future__ import absolute_import
from __future__ import print_function
#importing printlog() wrapper
from .debug import printlog

from six.moves import range
bstr_pos = lambda n: n>0 and bstr_pos(n>>1)+str(n&1) or ''

class BitStuffContext:
    def __init__(self):
        self.outbound = ""
        self.register = 0
        self.bits = 0
        self.ones = 0

    def push(self):
        self.outbound += chr(self.register)
        self.register = self.bits = self.ones = 0

    def _store_bit(self, bit):
        self.register <<= 1
        if bit:
            self.register |= 0x01
            self.ones += 1
        else:
            self.ones = 0
        printlog(("Register: %s" % bstr_pos(self.register)))
        self.bits += 1
        if self.bits == 8:
            printlog("Ax25","      : Pushing")
            self.push()

    def store_bit(self, bit):
        if bit and self.ones == 5:
            printlog("Ax25","      : Stuffing!")
            self._store_bit(0)
        self._store_bit(bit)

    def get_output(self):
        if self.bits:
            for i in range(self.bits, 8):
                self.store_bit(0)
        return self.outbound

def bitstuff(data):
    ctx = BitStuffContext()

    for byte in data:
        for bit in range(0,8):
            ctx.store_bit(ord(byte) & (1 << bit))

    return ctx.get_output()

if __name__ == "__main__":
    from d_rats.utils import hexprintlog

    data = "\xFF\xFF\xFF"

    printlog("Ax25","      : Start:")
    hexprintlog(data)

    printlog("Ax25","      \nStuffed:")
    hexprintlog(bitstuff(data))
