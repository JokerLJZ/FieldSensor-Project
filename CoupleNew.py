"""Create the calculation function."""

from math import (sqrt, pi, log10)
from numpy import interp
from scipy.special import fresnel

from Access import Access


def CalHighFreq(freq=None, field=None, dist=0.7):
    """Get the target power of couple port of the coupler.


       ==============  =======================================================
       **Argument:**
       freq            Defalt is None, input unit is GHz, range: 0.96, 18.
       field           Defalt is None, input unit is V/m.
       ==============  =======================================================
    """
    db = Access("/Data/BasicInfo.accdb")
    antenna = db.GetTableContent("ETSHorn", "天线型号, 频率下限, 频率上限, VSWR,"
                                 "口面宽A, 口面高B, 波导宽a, 波导高b,"
                                 "喇叭高度L, 斜高le, 斜高lh, 距离")
    horn = list(map(list, zip(*antenna)))
    couple = db.GetTableContent("HighFreqCouple", "Frequency, Coupling, ID,"
                                "Insertion, Difference")
    couple = list(map(list, zip(*couple)))
    if freq < 0.96 or freq > 18 or freq is None:
        raise ValueError("Wrong input freq of CalFieldHigh function.")
    elif freq == 0.96:
        antenna = horn[0][0]
    else:
        i = horn[2].index([x for x in horn[2] if freq < x][0])
        antenna = horn[0][i]
        vswr = horn[3][i]
        a = horn[4][i] / 100
        b = horn[5][i] / 100
        le = horn[9][i] / 100
        lh = horn[10][i] / 100
        d = dist  # 轴线上测量点到口面中心的距离
    s11 = (vswr - 1) / (vswr + 1)
    factor_input = 1 - pow(s11, 2)
    le1 = d * le / (le + d)
    lh1 = d * lh / (lh + d)
    lam = 0.3 / freq
    w = b / sqrt(2 * lam * le1)
    u = sqrt(lam * lh1 * 0.5) / a + a / sqrt(2 * lam * lh1)
    v = sqrt(lam * lh1 * 0.5) / a - a / sqrt(2 * lam * lh1)
    c_w = fresnel(w)[1]
    s_w = fresnel(w)[0]
    c_u = fresnel(u)[1]
    s_u = fresnel(u)[0]
    c_v = fresnel(v)[1]
    s_v = fresnel(v)[0]
    r_e = (pow(c_w, 2) + pow(s_w, 2)) / pow(w, 2)
    r_h = (0.25 * pow(pi, 2) * (pow(c_u - c_v, 2) +
           pow(s_u - s_v, 2)) / pow(u - v, 2))
    gain_0 = 32 * a * b / (pi * pow(lam, 2))  # 这个实际上也不是其远场增益
    gain_near = gain_0 * r_e * r_h  # 在设定条件下的近场增益
    p_in = 1  # 端口的射频功率
    e_cal_1w = sqrt(30 * gain_near * factor_input * p_in) / d

    # 以下进行功率计监控部分的处理
    freq_coupler = couple[0]
    powerratio_db_coupler = couple[4]  # 功率比值，dB
    freq *= pow(10, 9)
    # yi = interp1(x,Y,xi)
    power_ratio = interp(freq, freq_coupler, powerratio_db_coupler)
    pin_ambition = pow(field * d, 2) / (30 * gain_near * factor_input)
    pin_ambition_dbm = 10 * log10(pin_ambition) + 30
    p_meter_disp_dbm = pin_ambition_dbm - power_ratio

    return {"PowerMeter": p_meter_disp_dbm, "Antenna": antenna,
            "ECal": e_cal_1w}


def CalLowFreq(freq=None, field=None):
    """
       ==============  =======================================================
       **Argument:**
       freq            Defalt is None, input unit is MHz, range: 10, 1000.
       field           Defalt is None, input unit is V/m.
       ==============  =======================================================
    """
    db = Access("/Data/BasicInfo.accdb")

    couple = db.GetTableContent("LowFreqCouple", "Frequency, Coupling, ID,"
                                "Insertion, Difference")
    couple = list(map(list, zip(*couple)))

    if freq < 1 or freq > 1000 or freq is None:
        raise ValueError("Wrong freq input in CalLowFreq function.")
    elif 1 < freq < 250:
        b = 0.1489
        db.cursor.execute("SELECT * FROM TemZ WHERE Frequency=%f " % freq)
        temrow = db.cursor.fetchall()
        temall = db.GetTableContent("TemZ", "Frequency, Impedance, Phase")
        temall = list(map(list, zip(*temall)))
        if bool(temrow):
            temrow = list(temrow[0])
            z = temrow[1]
            phase = temrow[2]
        else:
            freqall = temall[0]
            zall = temall[1]
            phaseall = temall[2]
            z = interp(freq, freqall, zall)
            phase = interp(freq, freqall, phaseall)
    else:
        b = 0.07155
        db.cursor.execute("SELECT * FROM uTemZ WHERE Frequency=%f " % freq)
        utemrow = db.cursor.fetchall()
        utemall = db.GetTableContent("uTemZ", "Frequency, Impedance, Phase")
        utemall = list(map(list, zip(*utemall)))
        if bool(utemrow):
            utemrow = list(utemrow[0])
            z = utemrow[1]
            phase = utemrow[2]
        else:
            freqall = utemall[0]
            zall = utemall[1]
            phaseall = utemall[2]
            z = interp(freq, freqall, zall)
            phase = interp(freq, freqall, phaseall)
    freq_couple = couple[0]
    powerratio_db_coupler = couple[4]  # 功率比值，dB
    power_ratio_antenna2pm_db = interp(freq * 1e6, freq_couple,
                                       powerratio_db_coupler)
    pin_ambition = pow((field * b), 2) * phase / z
    pin_ambition_dbm = 10 * log10(pin_ambition) + 30
    p_meter_disp_dbm = pin_ambition_dbm - power_ratio_antenna2pm_db
    return {"PowerMeter": p_meter_disp_dbm}


if __name__ == "__main__":
    print(CalHighFreq(2, 20))
    # print(CalLowFreq(10, 20))
