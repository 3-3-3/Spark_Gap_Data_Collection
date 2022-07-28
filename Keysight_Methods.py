import pyvisa
import numpy as np
import matplotlib.pyplot as plt

def get_data_channels(inst, points='MAX', channels=[1]):
    '''
    Method to load data from multiple channels on Keysight Oscilliscope 3000-x
    (tested on MSOX3104T) into numpy array

    inst: pyvisa instrument instance of keysight oscilliscope
    points: number of points to collect. Default is the maximum allowed.
    channels: list of channels to collect from. Default is the first channel.

    Returns: Numpy array with rows: time, channel 1, channel 2...
    '''

    data = np.array([])

    for channel in channels:
        inst.write(':WAVeform:POINts:MODE RAW')
        inst.write(f':WAVeform:POINts {points}')
        inst.write(f':WAVeform:SOURce CHANnel{channel}')
        #Pull  binary data, and then convert on computer for speed
        inst.write(':WAVeform:FORMat BYTE')

        #Includes information for recovering voltage and time data
        #from raw binary data
        #see https://www.keysight.com/us/en/assets/9018-06894/programming-guides/9018-06894.pdf?success=true
        #pp. 1008
        preamble = inst.query(':WAVeform:PREamble?')
        (format, acq_type, n_points,
            avgcnt, t_inc, t_0,
            t_ref, y_inc,
            y_0, y_ref) = [float(i) for i in preamble.split(",")] #unpack information

        d = np.array(inst.query_binary_values(':WAVeform:DATA?', datatype='s'))
        d = (d - y_ref) * y_inc + y_0

        if channel == channels[0]:
            data = d
        else:
            data = np.vstack((data, d))

        #Each channel has the same time scale
        #so only do this once
        if channel == channels[-1]:
            t_max = (t_inc - t_ref) * data.shape[1] + t_0
            t = np.linspace(t_0, t_max, data.shape[1])

            data = np.vstack((t,data))

    return data

def get_data(inst, points='MAX', channel=1):
    '''
    Method to load data a single channels on Keysight Oscilliscope 3000-x
    (tested on InfiniiVision MSOX3104T) into numpy array

    inst: pyvisa instrument instance of keysight oscilliscope
    points: number of points to collect. Default is the maximum allowed.
    channel: channel to pull data from.

    Returns: Numpy array with rows: time, channel
    '''

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
