import numpy as np
import socket
import json
from datetime import datetime


class ADSBScratchDecoder:
    def __init__(self,output_ports,output_formats):
        self.output_ports=output_ports
        self.output_formats=[fmt.strip().lower() for fmt in output_formats.split(',')]
        self.sockets={}
        self._setup_sockets()
    
    def _setup_sockets(self):
        for fmt in self.output_formats:
            port=self.output_ports.get(fmt)
            if not port:
                print(f"NO PORT IDENTIFIED FOR FORMAT: {fmt}, SKIPPING")
                continue

            try:
                sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.sockets[fmt]=sock
                print(f"UDP socket created for {fmt} on port {port}")

            except Exception as e:
                print(f"ERROR SETTING UP SOCKET for {fmt} on port {port}: {e}")
                self.scockets[fmt]=None


    def crc_check(msg_bits):
    # Generator polynomial for ADS-B CRC-24
        GEN = 0x864CFB  

    # Convert list of bits -> integer, then append 24 zeros
        data = int("".join(str(b) for b in msg_bits), 2) << 24  

    # Go through the first 88 bits (data part of 112-bit ADS-B message)
        for _ in range(88):
        # If the top bit (bit 112) is set, XOR with generator aligned at top
            if data & (1 << (112 - 1)):  
                data ^= GEN << (112 - 24 - 1)  
        # Shift left to check next bit
            data <<= 1

    # If CRC remainder is 0, the message is valid
        return (data & 0xFFFFFF) == 0

    

    def format_message(self,message_data,fmt):
        icao=message_data.get('icao','N/A')
        alt=message_data.get('altitude','N/A')
        lat=message_data.get('latitude','N/A')
        lon=message_data.get('longitue','N/A')

        if fmt=='beast':
            return f"BEAST,{icao},{alt},{lat},{lon}\n"
        elif fmt=='sbs':
            return f"MSG,1,1,{icao},,,{datetime.now().strftime('%Y/%m/%d,%H:%M:%S.%f')},,,,,,{alt},{lat},{lon},,,,,,,,\n"
        elif fmt=='json':
            return json.dumps(message_data)
        else:
            return None
        
    def decode_and_output(self,samples):
        #1. Demodulation: convert IQ samples to magnitude
        mag=np.abs(samples)

        #2.pulse Detection: Find potential start of the message
        threshold=np.mean(mag)*2.5
        message_start_indices=np.where(mag>threshold)[0]


        for i in message_start_indices:
            #check of complete 112 bit message plus preamble
            #112 bits*2 chips/bit*2.4 MS/s sample rate=9.33 smaples.bit
            #so,~112*(2.4e6/1e6)=268smaples/message
            #preamble is 8 microseconds =8*2.4=19.2 smaples

            if i+268<len(mag):
                message_samples=mag[i:1+268]


                bits=[]
                for j in range(8,12):
                    chip_pair=message_samples[j*2,j*2+2]
                    if chip_pair[0]>chip_pair[1]:
                        bits.append(1)
                    else:
                        bits.append(0)

                if len(bits)==112:
                    if self.crc_check(bits):
                        icao_bin="".join(map(str,bits[8,32]))
                        icao_hex=f"{int(icao_bin,2):X}"

                        decoded_msg={
                            'icao':icao_hex,
                            ##--update
                        }
                        self.send_to_sockets(decoded_msg)


    def send_to_sockets(self,decoded_message):
        for fmt,sock in self.sockets.items():
            if not sock:
                continue

            formatted_data=self.format_message(decoded_message,fmt)

            if formatted_data:
                port=self.output_ports.get(fmt)
                try:
                    sock.sendto(formatted_data.encode('utf-8'),('127.0.0.1',port))
                except Exception as e:
                    print(f"Error sending {fmt} data: {e}")






        



        







   