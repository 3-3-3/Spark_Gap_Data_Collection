import pyvisa
import numpy as np
from Keysight_Methods import get_data, get_data_channels
import os


if __name__ == '__main__':
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

    print(f'[*] Getting data from channels: {channels}')
    data = get_data_channels(inst, channels=channels)

    print(f'[*] Writing data to: {f_name}')
    with open(f_name, 'wb') as f:
        np.save(f, data)

    print(f'[*] Closing instance: {inst}')
