import pyvisa
import numpy as np
from Keysight_Methods import get_data, get_data_channels
import os
import sys
import matplotlib.pyplot as plt
from datetime import date


if __name__ == '__main__':
    args = sys.argv
    today = date.today()

    save_dir = 'Breakdown_Measurements_LED_Alluminum'
    sub = f'G0.05mm_V1000V_LED_Pulse_Aluminum_370hz{today.month}_{today.day}'
    dir = os.path.join(save_dir, sub)
    trial = 1
    f_name = os.path.join(dir, f'trial_{trial}.npy')


    try:
        os.mkdir(save_dir)
    except:
        pass


    try:
        os.mkdir(dir)
    except:
        pass

    while os.path.exists(f_name):
        trial += 1
        f_name = os.path.join(dir, f'trial_{trial}.npy')


    rm = pyvisa.ResourceManager()
    addy = rm.list_resources()[0]
    inst = rm.open_resource(addy)
    inst.timeout = 15000
    channels = [1,3,4]

    if len(args) > 1:
        if args[1] == 'verbose':
            print(f'[*] Getting data from channels: {channels}')
            data = get_data_channels(inst, channels=channels)
            data[0] = data[0] * 160

            print(f'[*] Writing data to: {f_name}')
            with open(f_name, 'wb') as f:
                np.save(f, data)

            print(f'[*] Closing instance: {inst}')

            print(f'[*] Displaying data')

            for channel in data[1:data.shape[0]]:
                plt.plot(data[0], channel)
                plt.grid()
            plt.show()

    else:
        data = get_data_channels(inst, channels=channels)
        with open(f_name, 'wb') as f:
            np.save(f, data)
