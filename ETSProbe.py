""""Using visa manipulate the antenna controller. """

import ctypes
from ctypes import *
import time

__author__ = 'TheJoker'


class ETSProbe(object):
    """"""
    def __init__(self, port=5):
        self.probe = ctypes.windll.LoadLibrary('ETSProbe.dll')
        self.status = c_int()
        self.probeNo = c_char_p(b'probe1')
        self.port = c_char_p(b'com%s' % port)
        self.handle = c_int()
        self.family = c_char_p(b'HI-Any')
        self.battery = c_int()
        self.xfield = c_float()
        self.yfield = c_float()
        self.zfield = c_float()
        self.xyzfield = c_float()
        self.serialnum = c_char()
        self.arraysize = c_int(8)
        self.probe.ETS_CreateProbe(
            self.probeNo, byref(self.handle), self.port, self.family)

    def ProbeStatus(self):
        self.status = self.probe.ETS_ProbeStatus(self.handle)
        print(self.status)
        return self.status

    def ProbeBattery(self):
        self.probe.ETS_ReadBatterySynchronous(self.handle, byref(self.battery))
        self.battery = self.battery.value
        print(self.battery)
        return self.battery

    def ProbeField(self):
        self.probe.ETS_ReadFieldSynchronous(
            self.handle, byref(self.xfield), byref(self.yfield),
            byref(self.zfield), byref(self.xyzfield))
        field = [
            self.xfield.value, self.yfield.value,
            self.zfield.value, self.xyzfield.value]
        return field

    def ProbeSerial(self):
        self.probe.ETS_SerialNumber(
            self.handle, byref(self.serialnum), self.arraysize)
        self.serialnum = self.serialnum.value
        print(self.serialnum)
        return self.serialnum

    def RemoveProbe(self):
        self.probe.ETS_RemoveProbe(self.handle)


if __name__ == '__main__':
    probe = ETSProbe()
    probe.ProbeStatus()
    probe.ProbeBattery()
    probe.ProbeSerial()
    for i in range(1):
        time.sleep(2)
        print(probe.ProbeField())
    probe.RemoveProbe()
