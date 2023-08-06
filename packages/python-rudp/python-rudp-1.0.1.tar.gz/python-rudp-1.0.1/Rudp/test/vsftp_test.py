"""
Created on May 12, 2013

@author: SauliusAlisauskas
"""

import unittest

from Rudp import vsftp


class TestSequenceFunctions(unittest.TestCase):
    def testPacketTypeBegin(self):
        vsFtpPacket = vsftp.VsPacket()
        vsFtpPacket.type = vsftp.VsPacket.TYPE_BEGIN
        vsFtpPacket.data = "this must be a file name"
        packed = vsFtpPacket.pack()

        packet2 = vsftp.VsPacket().unpack(packed)
        self.assertEqual(vsFtpPacket.type, packet2.type,
                         "Type were not the same " + self._printPackets(vsFtpPacket, packet2))
        self.assertEqual(vsFtpPacket.data, packet2.data,
                         "Data was not the same " + self._printPackets(vsFtpPacket, packet2))

    def testPacketTypeData(self):
        vsFtpPacket = vsftp.VsPacket()
        vsFtpPacket.type = vsftp.VsPacket.TYPE_DATA
        vsFtpPacket.data = "this must be a file name"
        packed = vsFtpPacket.pack()

        packet2 = vsftp.VsPacket().unpack(packed)
        self.assertEqual(vsFtpPacket.type, packet2.type,
                         "Type were not the same," + self._printPackets(vsFtpPacket, packet2))
        self.assertEqual(vsFtpPacket.data, packet2.data,
                         "Data was not the same " + self._printPackets(vsFtpPacket, packet2))

    def testPacketTypeEnd(self):
        vsFtpPacket = vsftp.VsPacket()
        vsFtpPacket.type = vsftp.VsPacket.TYPE_END
        packed = vsFtpPacket.pack()

        packet2 = vsftp.VsPacket().unpack(packed)
        self.assertEqual(vsFtpPacket.type, packet2.type,
                         "Type were not the same," + self._printPackets(vsFtpPacket, packet2))
        self.assertEqual(vsFtpPacket.data, packet2.data,
                         "Data was not the same " + self._printPackets(vsFtpPacket, packet2))

    def _printPackets(self, vsFtpPacket, packet2):
        return "Packet:" + str(vsFtpPacket) + " unpacked:" + str(packet2)


if __name__ == '__main__':
    unittest.main()
