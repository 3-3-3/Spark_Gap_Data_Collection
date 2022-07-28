import pyvisa
import numpy as np
import matplotlib.pyplot as plt

def get_data_channels(inst, points='MAX', channels=[1]):
    #Set
    inst.write(f':WAVeform:POINts {points}')
    points = int(inst.query(f':WAVeform:POINts?'))
    data = np.array([])

    for channel in channels:
        inst.write(':WAVeform:POINts:MODE RAW')
        inst.write(f':WAVeform:SOURce CHANnel{channel}')
        inst.write(':WAVeform:FORMat BYTE')


        preamble = inst.query(':WAVeform:PREamble?')
        (wav, acq, wfmpts,
            avgcnt, t_inc, t_0,
            x_ref, y_inc, y_origin, y_ref) = [float(i) for i in preamble.split(",")]

        d = np.array(inst.query_binary_values(':WAVeform:DATA?', datatype='s'))
        d = (d - y_ref) * y_inc + y_origin

        if channel == channels[0]:
            data = d
        else:
            data = np.vstack((data, d))


        if channel == channels[-1]:
            t_max = t_inc * data.size
            t = np.linspace(t_0, t_max, data.shape[1])

            data = np.vstack((t,data))

    return data.transpose()

def get_data(inst, points='MAX', channel=1):
    inst.write(':WAVeform:POINts:MODE RAW')
    inst.write(f':WAVeform:POINts {points}')
    inst.write(f':WAVeform:SOURce CHANnel{channel}')
    inst.write(':WAVeform:FORMat BYTE')

    preamble = inst.query(':WAVeform:PREamble?')
    (wav, acq, wfmpts,
        avgcnt, t_inc, t_0,
        x_ref, y_inc, y_origin, y_ref) = [float(i) for i in preamble.split(",")]

    data = np.array(inst.query_binary_values(':WAVeform:DATA?', datatype='s'))
    data = (data - y_ref) * y_inc + y_origin

    t_max = t_inc * data.size
    t = np.linspace(t_0, t_max, data.size)

    return np.array([t, data])
