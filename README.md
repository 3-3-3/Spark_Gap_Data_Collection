# Spark_Gap_Data_Collection
Repository with code for data collection and analysis on our spark gap expirements. Has code for efficiently loading data from Keyskope 3000-x series oscilliscopes directly to numpy arrays, functions used in data analysis, raw data saved as .npy files, and a few Jupyter Notebooks which were used in data analysis.

The code for efficiently getting data from a Keysight 3000-x series oscilliscope to a computer is built using Pyvisa and Keysight IO Libraries Suite software. This code will likely be useful for future data collection using our Keyscope Oscilliscope, so it might be worth packaging this into its own repository at some point, but I am too lazy right now. Unfortunatly, the use of Keysight IO limits usage of the data collection code to Windows and Linux. For information on setting up Keysight IO Libraries Suite software and connecting to an oscilliscope, see the setting up section (Chapter 2) of the [Keysight programming guide](https://www.keysight.com/us/en/assets/9018-06894/programming-guides/9018-06894.pdf?success=true).

Pyvisa can easily be installed with pip:

```pip install pyvisa```

For more information on Pyvisa, here is a link to their [documentation](https://pyvisa.readthedocs.io/en/latest/introduction/rvalues.html).

Currently, there are three program files related to data collection. Controller.py more or less updates the legacy example code given in the Keysight programming guide (see chapter 40). This follows the structure that Keysight recommends for "every program you will write for the oscilliscope"–namely an initialization routine, a capture routine, and an analyze routine. This structure is useful if you want to completely automate the oscilliscope; the initialization routine will consistently set the oscilliscope triggers, scales etc., the capture routine makes sure data is collected, and the analyze routine is meant to analyze or collect the data. 

What we really want though is to use the oscilliscope as normal and then just be able to easily load the data it collects into a numpy array. This is what the methods in Keysight_Methods.py do. These assume that the user has collected data already and captured a sweep, and then queries the binary data from the oscilliscope, and does some calculations to convert that data back to the original time and voltage data (see e.g. page 1008 of the Keysight programming guide). Two methods are included; here is an example of their usage:

```
import pyvisa
from Keysight_Methods import get_data, get_data_channels

rm = pyvisa.ResourceManager()
addy = rm.list_resources()[0]
inst = rm.open_resource(addy)

all_channels = get_data_channels(inst, points=5000, channels=[1,2,3,4])
channel_2 = get_data(inst, points='MAX', channel=2)
```

This code uses pyvisa to open a connection to the first instrument VISA Address resource manager finds; if you are connected to multiple instruments, you will need to figure out which is which (just print out rm.list_resources, and compare with the VISA Address of your instruments). It then uses get_data_channels to get a numpy array called all_channels, where the first row will be the time, and each subsequent row will be the subsequent voltage reading from each channel, and 5000 points will be sampled. The next line uses get_data to instantiate an array where the first row is the time and the next is the corresponding data from channel 2; the maximum number of points (2,000,000 points on the InfiniiVision MSOX3104T oscilliscope) will be sampled. Note that this MAX option is the default for both methods. 

The file Spark_Gap_Data_Collector.py is specifically for obtaining data from the spark gap, and uses get_data_channels to query oscilliscope data, and also saves and offers initial visualization fo the data. 

Data is collected in measurement directories. Generally, these are further organized into subfolders whose names offer information about the expirement parameters as well as the date which data was taken. The actual data is then save in files named "trial_x.npy" where x is sequential for the specific directory.

The functions in analysis_functions.py were used in data analysis, and include functions for loading data in useful ways, functions for detecting discharges (relatively large changes in voltage; the user must specifify what constitutes large), spliting collected data into discharge frames, fitting functions, and a veriety of others. 

The jupyter notebooks include the actual data analysis conducted. As Jupyter Notebooks have a tendency to do, it is not super organized, but gets the job done. The notebooks should at least be reproducable in sequential order, which, if I'm being honest, is not always the case with my notebooks (e.g. run cell 31, then cell 15, then all the others skipping cells 15, 16, 45, and 50, but make sure to rerun cell 31). 

There is some other clutter I should get rid of which is just saved plots etc., and .DS_Store files which I seriously need to remember to add to .gitignore.
