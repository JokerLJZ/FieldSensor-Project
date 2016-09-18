"""Using visa manipulate the NRP power sensor. All unit is MHz and dBm."""

import logging
import traceback
import time
from math import log10

__author__ = 'TheJoker'


class PMNRP(object):
    "All unit input is MHz and dBm."

    def __init__(self, nrpaddr, resourcemanager=None):

        if resourcemanager is None:
            self.rm = visa.ResourceManager()
        else:
            self.rm = resourcemanager
        self.Log()
        try:
            self.PM = self.rm.open_resource(nrpaddr)
        finally:
            self.logger.error(traceback.format_exc())
        self.NRPRange = [-67, 23]
        self.value = -85

    def Log(self):
        """Initialise the log function."""
        self.logger = logging.getLogger()
        handler = logging.FileHandler("Data\\TestLog.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s -%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def PMState(self):
        idn = self.PM.query('*IDN?')
        if 'NRP' in idn:
            return True
        else:
            return False

    def PMQuery(self, order):
        return self.PM.query(order)

    def PMWrite(self, order):
        self.PM.write(order)

    def PMRead(self, order):
        self.PM.write(order)
        return self.PM.read()

    def PMClose(self):
        self.PM.close()

    def PMInRange(self, power):
        if self.NRPRange[0] <= power <= self.NRPRange[1]:
            return True
        else:
            return False

    def PMCal(self):
        """Calibrate and zero the power sensor"""
        zerocommand = 'CALibration:ZERO:AUTO ONCE'
        self.PMWrite(zerocommand)

    def PMSetFreq(self, freq=1e3):
        """Set the frequency and return the frequency number.

        ===============   =============================================
        **Argument:**
        state             Defalt is False,.
        ===============   =============================================
        """
        freq = freq * 1e6
        freqcommand = 'SENSe:FREQuency'
        freqwrite = freqcommand + ' ' + str(freq)
        freqquery = freqcommand + '?'
        self.PMWrite(freqwrite)
        return self.PMQuery(freqquery)

    def PMAVERageRESet(self):
        """Reset the average state"""
        self.PMWrite('SENSe:AVERage:RESet')

    def PMAVERageState(self, state=False):
        """Set the average state and return the state.

        ===============   =============================================
        **Argument:**
        state             Defalt is False, if True open the pm average,
                          if False close it.
        ===============   =============================================
        """
        if state is True:
            self.PMWrite('SENSe:AVERage:STATe ON')
            return 'Average state on'
        elif state is False:
            self.PMWrite('SENSe:AVERage:STATe OFF')
            return 'Average state off'
        else:
            self.logger.error(
                "Wrong command input to PMAVERageState function in class"
                "PMNARP.")
            raise ValueError(
                "Wrong command input to PMAVERageState function in class"
                "PMNARP.")

    def PMFetch(self):
        """Fetch the power value, and return the power in dBm."""
        self.PMWrite('INIT:IMM')
        time.sleep(2)
        result = self.PMQuery('FETCH?')
        value = float(result.split(',')[0])
        if value < 1e-12:
            return -150.0  # Clip noise
        else:
            return 10.0 * log10(value) + 30.0


if __name__ == '__main__':
    import visa
    rm = visa.ResourceManager()
    NRPtest = PMNRP('RSNRP::0x0021::101975::INSTR', rm)

    print(NRPtest.PMQuery('*IDN?'))
    #    NRPtest.PACal()
    print(NRPtest.PMSetFreq(250000000))
    for i in range(100):
        print(NRPtest.PMFetch())
    # print(NRPtest.PMFetch())
    NRPtest.PMClose()
