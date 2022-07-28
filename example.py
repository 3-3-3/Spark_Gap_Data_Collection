#!python3
# *********************************************************
# This program illustrates a few commonly-used programming
# features of your Keysight oscilloscope.
# *********************************************************
# Import modules.
# ---------------------------------------------------------
import pyvisa
import string
import struct
import sys
# Global variables (booleans: 0 = False, 1 = True).
# ---------------------------------------------------------
debug = 0
# =========================================================
# Initialize:
# =========================================================
def initialize():
    # Get and display the device's *IDN? string.
    idn_string = do_query_string("*IDN?")
    print(f"Identification string: '{idn_string}'")
    # Clear status and load the default setup.
    do_command("*CLS")
    do_command("*RST")

# =========================================================
# Capture:
# =========================================================
def capture():
    # Use auto-scale to automatically set up oscilloscope.
    print("Autoscale.")
    do_command(":AUToscale")
    # Set trigger mode.
    do_command(":TRIGger:MODE EDGE")
    qresult = do_query_string(":TRIGger:MODE?")
    print("Trigger mode: %s" % qresult)
    # Set EDGE trigger parameters.
    do_command(":TRIGger:EDGE:SOURce CHANnel1")
    qresult = do_query_string(":TRIGger:EDGE:SOURce?")
    print("Trigger edge source: %s" % qresult)
    do_command(":TRIGger:EDGE:LEVel 1.5")
    qresult = do_query_string(":TRIGger:EDGE:LEVel?")
    print("Trigger edge level: %s" % qresult)
    do_command(":TRIGger:EDGE:SLOPe POSitive")
    qresult = do_query_string(":TRIGger:EDGE:SLOPe?")
    print("Trigger edge slope: %s" % qresult)
    # Save oscilloscope setup.
    sSetup = do_query_ieee_block(":SYSTem:SETup?")
    f = open("setup.stp", "wb")
    f.write(sSetup)
    f.close()
    print("Setup bytes saved: %d" % len(sSetup))
    # Change oscilloscope settings with individual commands:
    # Set vertical scale and offset.
    do_command(":CHANnel1:SCALe 0.05")
    qresult = do_query_string(":CHANnel1:SCALe?")
    print("Channel 1 vertical scale: %s" % qresult)
    do_command(":CHANnel1:OFFSet -1.5")
    qresult = do_query_string(":CHANnel1:OFFSet?")
    print("Channel 1 offset: %s" % qresult)
    # Set horizontal scale and offset.
    do_command(":TIMebase:SCALe 0.0002")
    qresult = do_query_string(":TIMebase:SCALe?")
    print("Timebase scale: %s" % qresult)
    do_command(":TIMebase:POSition 0.0")
    qresult = do_query_string(":TIMebase:POSition?")
    print("Timebase position: %s" % qresult)
    # Set the acquisition type.
    do_command(":ACQuire:TYPE NORMal")
    qresult = do_query_string(":ACQuire:TYPE?")
    print("Acquire type: %s" % qresult)
    # Or, set up oscilloscope by loading a previously saved setup.
    sSetup = ""
    f = open("setup.stp", "rb")
    sSetup = f.read()
    f.close()
    do_command_ieee_block(":SYSTem:SETup", sSetup)
    print("Setup bytes restored: %d" % len(sSetup))
    # Capture an acquisition using :DIGitize.
    do_command(":DIGitize CHANnel1")


# =========================================================
# Analyze:
# =========================================================
def analyze():
    # Make measurements.
    # --------------------------------------------------------
    do_command(":MEASure:SOURce CHANnel1")
    qresult = do_query_string(":MEASure:SOURce?")
    print("Measure source: %s" % qresult)
    do_command(":MEASure:FREQuency")
    qresult = do_query_string(":MEASure:FREQuency?")
    print("Measured frequency on channel 1: %s" % qresult)
    do_command(":MEASure:VAMPlitude")
    qresult = do_query_string(":MEASure:VAMPlitude?")
    print("Measured vertical amplitude on channel 1: %s" % qresult)
    # Download the screen image.
    # --------------------------------------------------------
    do_command(":HARDcopy:INKSaver OFF")
    sDisplay = do_query_ieee_block(":DISPlay:DATA? PNG, COLor")
    # Save display data values to file.
    f = open("screen_image.png", "wb")
    f.write(sDisplay)
    f.close()
    print("Screen image written to screen_image.png.")
    # Download waveform data.
    # --------------------------------------------------------
    # Set the waveform points mode.
    do_command(":WAVeform:POINts:MODE RAW")
    qresult = do_query_string(":WAVeform:POINts:MODE?")
    print("Waveform points mode: %s" % qresult)
    # Get the number of waveform points available.
    do_command(":WAVeform:POINts 10240")
    qresult = do_query_string(":WAVeform:POINts?")
    print("Waveform points available: %s" % qresult)
    # Set the waveform source.
    do_command(":WAVeform:SOURce CHANnel1")
    qresult = do_query_string(":WAVeform:SOURce?")
    print("Waveform source: %s" % qresult)
    # Choose the format of the data returned:
    do_command(":WAVeform:FORMat BYTE")
    print("Waveform format: %s" % do_query_string(":WAVeform:FORMat?"))
    # Display the waveform settings from preamble:
    wav_form_dict = {
        0 : "BYTE",
        1 : "WORD",
        4 : "ASCii",
    }
    acq_type_dict = {
        0 : "NORMal",
        1 : "PEAK",
        2 : "AVERage",
        3 : "HRESolution",
    }
    preamble_string = do_query_string(":WAVeform:PREamble?")

    (
        wav_form, acq_type, wfmpts, avgcnt, x_increment, x_origin,
        x_reference, y_increment, y_origin, y_reference
    ) = preamble_string.split(",")

    print("Waveform format: %s" % wav_form_dict[int(wav_form)])
    print("Acquire type: %s" % acq_type_dict[int(acq_type)])
    print("Waveform points desired: %s" % wfmpts)
    print("Waveform average count: %s" % avgcnt)
    print("Waveform X increment: %s" % x_increment)
    print("Waveform X origin: %s" % x_origin)
    print("Waveform X reference: %s" % x_reference) # Always 0.
    print("Waveform Y increment: %s" % y_increment)
    print("Waveform Y origin: %s" % y_origin)
    print("Waveform Y reference: %s" % y_reference)
    # Get numeric values for later calculations.
    x_increment = do_query_number(":WAVeform:XINCrement?")
    x_origin = do_query_number(":WAVeform:XORigin?")
    y_increment = do_query_number(":WAVeform:YINCrement?")
    y_origin = do_query_number(":WAVeform:YORigin?")
    y_reference = do_query_number(":WAVeform:YREFerence?")
    # Get the waveform data.
    sData = do_query_ieee_block(":WAVeform:DATA?")
    # Unpack unsigned byte data.
    values = struct.unpack("%dB" % len(sData), sData)
    print("Number of data values: %d" % len(values))
    # Save waveform data values to CSV file.
    f = open("waveform_data.csv", "w")
    for i in range(0, len(values) - 1):
        time_val = x_origin + (i * x_increment)
        voltage = ((values[i] - y_reference) * y_increment) + y_origin
        f.write("%E, %f\n" % (time_val, voltage))
    f.close()
    print("Waveform format BYTE data written to waveform_data.csv.")

# =========================================================
# Send a command and check for errors:
# =========================================================
def do_command(command, hide_params=False):
    if hide_params:
        (header, data) = command.split(" ", 1)
    if debug:
        print("\nCmd = '%s'" % header)
    else:
        if debug:
                print("\nCmd = '%s'" % command)

    InfiniiVision.write("%s" % command)

    if hide_params:
        check_instrument_errors(header)
    else:
        check_instrument_errors(command)
# =========================================================
# Send a command and binary values and check for errors:
# =========================================================
def do_command_ieee_block(command, values):
    if debug:
        print("Cmb = '%s'" % command)

    InfiniiVision.write_binary_values("%s"%command, values, datatype='B'
    )

    check_instrument_errors(command)
# =========================================================
# Send a query, check for errors, return string:
# =========================================================
def do_query_string(query):
    if debug:
        print("Qys = '%s'" % query)
    result = InfiniiVision.query("%s" % query)
    check_instrument_errors(query)
    return result

# =========================================================
# Send a query, check for errors, return floating-point value:
# =========================================================
def do_query_number(query):
    if debug:
        print("Qyn = '%s'" % query)
    results = InfiniiVision.query("%s" % query)
    check_instrument_errors(query)
    return float(results)
# =========================================================
# Send a query, check for errors, return binary values:
# =========================================================
def do_query_ieee_block(query):
    if debug:
        print("Qys = '%s'" % query)
    result = InfiniiVision.query_binary_values("%s" % query, datatype='s')
    check_instrument_errors(query)
    return result[0]
# =========================================================
# Check for instrument errors:
# =========================================================
def check_instrument_errors(command):
    while True:
        error_string = InfiniiVision.query(":SYSTem:ERRor?")
        if error_string: # If there is an error string value.
            if error_string.find("+0,", 0, 3) == -1: # Not "No error".
                print("ERROR: %s, command: '%s'" % (error_string, command))
                print("Exited because of error.")
                sys.exit(1)
            else: # "No error"
                break
        else: # :SYSTem:ERRor? should always return string.
            print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)
            print("Exited because of error.")
            sys.exit(1)
# =========================================================
# Main program:
# =========================================================
rm = pyvisa.ResourceManager()
addy = rm.list_resources()[0]
InfiniiVision = rm.open_resource(addy)
InfiniiVision.timeout = 15000
InfiniiVision.clear()
# Initialize the oscilloscope, capture data, and analyze.
initialize()
capture()
analyze()
InfiniiVision.close()
print("End of program.")
sys.exit()
