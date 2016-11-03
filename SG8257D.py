""""Using visa manipulate the 8257D signal generator. """

import traceback

import visa

__author__ = 'TheJoker'


class SG8257D(object):
    "All unit input is MHz and dBm."

    def __init__(self, sgaddr="GIB0::19::INSTR", resourcemanager=None):
        """Initial the signal generator.

        ===============   =============================================
        **Argument:**
        sgaddr            Defalt is 19 which indicate the visa address:
                          "GPIB0::19::INSTR".
        resourcemanager   Defalt is None, if there is no resourcemanager
                          pass in to the object, the signal generator
                          object will create one by itself.
        ===============   =============================================
        """
        if resourcemanager is None:
            self.rm = visa.ResourceManager()
        else:
            self.rm = resourcemanager
        try:
            self.sg = self.rm.open_resource(sgaddr)
            self.SGWrite('*RST')
        finally:
            print("8257D信号源连接错误, 请进行系统检查!")

    def SGState(self):
        idn = self.sg.query('*IDN?')
        if '8257' in idn:
            return True
        else:
            return False

    def SGQuery(self, order):
        return self.sg.query(order)

    def SGWrite(self, order):
        self.sg.write(order)

    def SGRead(self, order):
        self.sg.write(order)
        return self.sg.read()

    def SGClose(self):
        self.sg.close()

    def SGInRange(self, power):
        powerrange = [-115, 25]
        if powerrange[0] <= power <= powerrange[1]:
            return True
        else:
            return False

    def SGRef(self, ref='INT'):
        """Set the reference osillator souce and return the status.

        ===============   ==============================================
        **Argument:**
        ref               defalt is INT, INT (internal) or EXT(external)
        ===============   ==============================================
        """
        ref += '\n'
        self.SGWrite(':ROSCillator:SOURce' + ' ' + ref)
        if self.SGQuery(':ROSCillator:SOURce?') == ref:
            return True
        else:
            return False

    def SGCWFrec(self, freq=5000):
        """Set the frequency of signal generator and return the value.

        ===============   =============================================
        **Argument:**
        Freq              Defalt is 5GHz, and unit is MHz
        ===============   =============================================
        """

        freq *= 10e6
        if 10000 <= freq <= 31800000000:
            freqcommand = ':FREQ'
            freqwrite = freqcommand + ' ' + str(freq)
            freqquery = freqcommand + '?'
            self.sg.write(freqwrite)
            return self.sg.query(freqquery)
        else:
            raise ValueError("Frequency out of range")

    def SGPowerSet(self, power=-125):
        """Set the power of signal generator and return the power value.

        ===============   ==================================================
        **Argument:**
        power             defalt is -125dBm, power should in range[-125, 25]
        ===============   ==================================================
        """
        if self.SGInRange(power):
            self.SGWrite(':POW' + ' ' + str(power))
        return self.SGQuery(':POW?')

    def SGPowerOut(self, state='OFF'):
        """set the RF ON or OFF.

        ===============   ==================================================
        **Argument:**
        state             default setting is OFf, state is "ON" or "OFF".
        ===============   ==================================================
        """
        if state is 'ON' or 'OFF':
            self.SGWrite(':OUTP ' + state)
            return 'SG power status: ' + state
        else:
            self.logger.error("Wrong order input in SGPowerOut function.")
            raise ValueError("Wrong order input in SGPowerOut function.")


if __name__ == '__main__':
    import visa
    rm = visa.ResourceManager()
    SGAddr = 'GPIB0::19::INSTR'
    SG = SG8257D(SGAddr, rm)
    print(SG.SGQuery('*IDN?'))
    freq = 1.5
    frequency = freq * 1000000000
    if 10000 <= frequency <= 31800000000:
        print('adfsdf')
    print(SG.SGCWFrec(frequency))
    print(SG.SGPowerSet(-20))
    print(SG.SGRef())
    print(SG.SGPowerOut('OFF'))
#    SG.SGClose()
