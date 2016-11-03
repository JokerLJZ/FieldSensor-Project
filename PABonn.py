"""Using visa manipulate the Bonn power amplifier. All unit is MHz."""

import logging
import visa
import traceback

__author__ = "Joker.Liu"


class PABonn(object):
    """Create a power amplifier object of Bonn."""

    def __init__(self, paaddr="GIB0::7::INSTR", resourcemanager=None):
        """Initial the bonn power amplifier.

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
            self.pa = self.rm.open_resource(paaddr)
        finally:
            print("BONN功放连接失败, 请进行系统检查!")

    def Log(self):
        """Initialise the log function."""
        self.logger = logging.getLogger()
        handler = logging.FileHandler("Data\\TestLog.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s -%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def PAState(self):
        """Retrun the power amplifier state."""
        idn = self.pa.query('*IDN?')
        if 'BONN' in idn:
            return True
        else:
            return False

    def PAQuery(self, order):
        """Return the """
        return self.pa.query(order)

    def PAWrite(self, order):
        self.pa.write(order)

    def PARead(self, order):
        self.pa.write(order)
        return self.pa.read()

    def PAClose(self):
        self.pa.close()

    def PABand(self, freq):
        """according the frequency set the band number.

        """
        freq /= 1000
        if 0.08 <= freq < 1:
            bandnum = 1
        elif 1 <= freq <= 2:
            bandnum = 2
        elif 2 < freq <= 6:
            bandnum = 3
        elif 6 < freq <= 18:
            bandnum = 4
        else:
            self.logger.error(
                "Wrong frequency input in function PABand of Class PABonn")
            raise ValueError(
                "Wrong frequency input in function PABand of Class PABonn")
        band = 'SW01_' + str(bandnum)
        self.PAWrite(band)
        self.PAWrite("*IDN?")
        return band

    def PAPowerOut(self, order='OFF'):
        """set the RF output state.

        ==============  =============================================
        **Argument:**
        order           Defalt is OFF, input should be 'ON' or 'OFF'.
        ==============  =============================================
        '"""
        if order is 'ON' or 'OFF':
            self.PAWrite('AMP_' + order)
            self.PAWrite('*IDN?')
            return 'SG power status: ' + order
        else:
            self.logger.error(
                "Wrong power input to PA in function PAPowerOut.")
            raise ValueError(
                "Wrong power input to PA in function PAPowerOut.")


if __name__ == "__main__":
    raise ValueError("dfa")
    pa = PABonn()
