import configparser
import numpy as np
from rtlsdr import RtlSdr
from decoder import ADSBScratchDecoder


def main():
    config =configparser.ConfigParser()
    config.read('config.ini')

    sdr_settings = config['SDR_SETTINGS']
    center_freq = sdr_settings.getint('center_freq')
    sample_rate = sdr_settings.getint('sample_rate')
    gain_val = sdr_settings.get('gain')
    freq_correction = sdr_settings.getint('freq_correction')
    read_size = sdr_settings.getint('read_size')

    output_ports = {key: int(val) for key, val in config['OUTPUT_PORTS'].items()}
    output_formats = config.get('GENERAL', 'output_formats')


    try:
        sdr=RtlSdr()
        sdr.sample_rate=sample_rate
        sdr.center_freq=center_freq
        if gain_val.lower()=='auto':
            sdr.gain='auto'
        else:
            sdr.gain=float(gain_val)
        sdr.freeq_correction=freq_correction

    except Exception as e:
        print(f"ERROR installing RTL-SDR {e}")
        return
    
    adsb_decoder=ADSBScratchDecoder(output_ports,output_formats)

    print("-----STARTING RTL-SDR DATA STREAM-----")

    try:
        while True:
            samples=sdr.read_samples(read_size)
            adsb_decoder.decode_and_output(samples)
    except KeyboardInterrupt:
        print("Stopping the program")
    except Exception as e:
        print(f"A error occured: {e}")
    finally:
        sdr.close()


if __name__=="__main__":
    main()
