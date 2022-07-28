import pyvisa
import sys
from Keysight_Methods import get_data

def initialize(instrument, fname=None):
    idn_string = instrument.query('*IDN?')
    print(f'[**] Initializing insturment: {idn_string}')
    if fname == None:
        print(f'[**] No init file given')
        print(f'[**] Clearing status')
        instrument.write('*CLS')
        print(f'[**] Loading default')
        instrument.write('*RST')


def capture(instrument):
    #try:
    print('[**] Autoscaling')
    instrument.write(':AUToscale')
    print('[**] Setting Trigger')
    instrument.write(':TRIGger:MODE EDGE')

    print(f"[**] Trigger mode: {instrument.query(':TRIGger:MODE?')}")
    instrument.write(':TRIGger:EDGE:SOURce CHANnel1')
    print(f"[**] Trigger source: {instrument.query(':TRIGger:EDGE:SOURce?')}")
    instrument.write(':TRIGger:EDGE:LEVel 1.5')
    print(f"[**] Trigger edge level: {instrument.query(':TRIGger:EDGE:LEVel?')}")
    instrument.write(':TRIGger:EDGE:SLOPe: POSitive')
    print(f"[**] Trigger edge slope: {instrument.query(':TRIGger:EDGE:SLOPe?')}")

    f_name = 'setup.stp'
    print(f'\n[**] Saving oscilliscope setup to: {f_name} \n')
    #with open(f_name, 'w') as f:
        #result = instrument.query_binary_values(':SYSTem:SETup?',datatype='s')
        #f.write(result[0])


    channel = 1
    instrument.write(f':CHANnel{channel}:SCALe 0.8')
    print(f"[**] Channel {channel} scale: {instrument.query(f':CHANnel{channel}:SCALe?')}")
    #instrument.write(f':CHANnel{channel}:OFFSet -1.5')
    #print(f"[**] Channel {channel} offset: {instrument.query(f':CHANnel{channel}:OFFSet?')}")




if __name__ == '__main__':
    rm = pyvisa.ResourceManager()
    addy = rm.list_resources()[0]
    print(f'[*] Scope addy: {addy}')
    print(f'[*] Initializing scope controller')
    inst = rm.open_resource(addy)
    inst.timeout = 15000
    print(f'[*] Begin initialization')
    initialize(inst)
    print('\n --- --- --- --- --- --- \n')
    print('[*] Capturing')
    capture(inst)
    print('[*] Getting data')
    get_data(inst,points=1000)
