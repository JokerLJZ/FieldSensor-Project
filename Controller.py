""""Using visa manipulate the antenna controller. """

import traceback
import time
import visa

__author__ = 'TheJoker'


class Controller(object):

    def __init__(self, ctaddr="GIB0::10::INSTR", resourcemanager=None):
        """Initial the antenna controller.

        ===============   =============================================
        **Argument:**
        ctaddr            Defalt is 10 which indicate the visa address:
                          "GPIB0::10::INSTR".
        resourcemanager   Defalt is None, if there is no resourcemanager
                          pass in to the object, the antenna controller
                          object will create one by itself.
        ===============   =============================================
        """
        if resourcemanager is None:
            self.rm = visa.ResourceManager()
        else:
            self.rm = resourcemanager
        try:
            self.CT2090 = self.rm.open_resource(ctaddr)
            self.CTWrite('N2;CL 0;WL 360')
            self.angle = self.CTReadAngel()
        finally:
            print("转台控制器连接错误, 请进行系统检查!")

    def CTQuery(self, order):
        return self.CT2090.query(order)

    def CTWrite(self, order):
        self.CT2090.write(order)

    def CTRead(self, order):
        self.CT2090.write(order)
        return self.CT2090.read()

    def CTClose(self):
        self.CT2090.close()

    def CTReadAngel(self):
        angle = self.CTRead('CP?')
        angle = float(angle[1:5])
        return angle

    def CTRoll(self, angle):
        """turn the table to the set angle.

        ===============   ===================================================
        **Argument:**
        angle             Defalt is None, if success return True, else return
                          False.
        ===============   ===================================================
        """
        waittime = 1
        rolldone = True
        angleorder = 'SK ' + str(angle)
        self.CTWrite(angleorder)
        while int(self.CTQuery('*OPC?')[0]) < 1:
            time.sleep(0.5)
            if waittime > 40:
                rolldone = False
                break
            waittime += 0.5
        return rolldone

    def CTAntennaRoll(self, antenna):
        """180: 02     90: 04       270: 03     360: 01"""
        if antenna == 316001:
            angel = self.CTReadAngel()
            if angel >= 180:
                self.CTRoll(360)
            else:
                self.CTRoll(0)
        elif antenna == 316002:
            self.CTRoll(180)
        elif antenna == 316003:
            self.CTRoll(268.8)
        else:
            self.CTRoll(89)

    def CTAntennaChange(self, antenna):
        """90: 02     0: 04       180: 03     270: 01"""
        if antenna == 316003:
            angel = self.CTReadAngel()
            if angel >= 180:
                self.CTRoll(360)
            else:
                self.CTRoll(0)
        elif antenna == 316004:
            self.CTRoll(180)
        elif antenna == 316001:
            self.CTRoll(90)
        else:
            self.CTRoll(270)

if __name__ == '__main__':
    rm = visa.ResourceManager()
    CTAddr = 'GPIB0::10::INSTR'
    CT = Controller(CTAddr, rm)
    print(CT.CTRoll(89))
    CT.CTClose()
