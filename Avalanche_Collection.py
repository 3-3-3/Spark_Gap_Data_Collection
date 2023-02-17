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


    save_dir = 'Avalanche_Transistor'
    sub = f'35kHZ_14.0V_Circuit1{today.month}_{today.day}'
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
    channel = 1


    if len(args) > 1:
        if args[1] == 'verbose':
            print(f'[*] Getting data from channels: {channel}')
            data = get_data(inst, points='MAX', channel=channel)
            data[0] = data[0]

            print(f'[*] Writing data to: {f_name}')
            with open(f_name, 'wb') as f:
                np.save(f, data)

            print(f'[*] Closing instance: {inst}')

            print(f'[*] Displaying data')


            plt.plot(data[0], data[1],marker='.')
            plt.grid()
            plt.show()

    else:
        data = get_data_channels(inst, channels=channels)
        with open(f_name, 'wb') as f:
            np.save(f, data)
