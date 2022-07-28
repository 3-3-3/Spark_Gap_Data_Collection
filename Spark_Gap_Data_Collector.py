import pyvisa
import numpy as np
from Keysight_Methods import get_data, get_data_channels
import os
import sys
import matplotlib.pyplot as plt


if __name__ == '__main__':
    args = sys.argv

    save_dir = 'NoLED'
    trial = 1
    f_name = os.path.join(save_dir, f'trial_{trial}.npy')

    try:
        os.mkdir(save_dir)
    except:
        pass

    while os.path.exists(f_name):
        trial += 1
        f_name = os.path.join(save_dir, f'trial_{trial}.npy')


    rm = pyvisa.ResourceManager()
    addy = rm.list_resources()[0]
    inst = rm.open_resource(addy)
    channels = [2,3]

    if len(args) > 1:
        if args[1] == 'verbose':
            print(f'[*] Getting data from channels: {channels}')
            data = get_data_channels(inst, channels=channels)

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
