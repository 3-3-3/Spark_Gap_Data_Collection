# Spark_Gap_Data_Collection
Small repository with code for efficiently getting data from a Keysight 3000-x series oscilliscope to a computer. It is built using Pyvisa and Keysight IO Libraries Suite software. Unfortunatly, the use of Keysight IO limits usage to Windows and Linux. For information on setting up Keysight IO Libraries Suite software and connecting to an oscilliscope, see the setting up section (Chapter 2) of the [Keysight programming guide](https://www.keysight.com/us/en/assets/9018-06894/programming-guides/9018-06894.pdf?success=true).

Pyvisa can easily be installed with pip:

```pip install pyvisa```

For more information on Pyvisa, here is a link to their [documentation](https://pyvisa.readthedocs.io/en/latest/introduction/rvalues.html).

Currently, there are three program files in this repository. Controller.py more or less updates the legacy python code given in the Keysight programming guide (see chapter 40). This follows the structure that Keysight gives (for "every program you will write for the oscilliscope"), namely an initialization routine, a capture routine, and an analyze routine. This structure is useful if you want to completely automate the oscilliscope; the initialization routine will consistently set the oscilliscope triggers, scales etc., the capture routine makes sure data is collected, and the analyze routine is meant to analyze or collect the data. 

What we really want though is to use the oscilliscope as normal and then just be able to easily load the data it collects into a numpy array, so that is what the metohods in Keysight_Methods.py do. These assume that the user has collected data already, and then queries the binary data from the oscilliscope, and does some calculations to convert that data back to the original time and voltage data (see e.g. page 1008 of the Keysight programming guide). Two methods are included; here is an example of their usage:

```
import pyvisa
from Keysight_Methods import get_data, get_data_channels

rm = pyvisa.ResourceManager()
addy = rm.list_resources()[0]
inst = rm.open_resource(addy)

all_channels = get_data_channels(inst, points=5000, channels=[1,2,3,4])
channel_2 = get_data(inst, points='MAX', channel=2)
```

This code uses pyvisa to open a connection to the first instrument VISA ID resource manager finds; if you are connected to multiple instruments, you will need to figure out which is which (just print out rm.list_resources, and compare with the VISA ID of your instruments). It then uses get_data_channels to get a numpy array called all_channels, where the first row will be the time, and the next for is each channel. 
