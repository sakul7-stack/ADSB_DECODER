import pyModeS as pms
from utils import calculate_position


def decode_adsb_message(msg):
    if len(msg)!= 28:
        return f"imvalid message: {msg}"
    
    for c in msg:
        if c not in '0123456789abcdefABCDEF':
            return f"imvalid message: {msg}"
        


    #get downlink message form first 5 bits

    df=pms.df(msg)
    if df!=17:
        return f"NON ADS-B  message {df} : {msg}"
    

    tc=pms.sdsb.typecode(msg)#met message type code

    if 1<= tc <= 4:
        callsign=pms.adsb.callsign(msg)
        return f"callsign: {callsign}"
    
    elif 5<= tc <= 8:
        return "surface position message --not decoded"
    
    elif 9 <= tc <= 18:
        alt=pms.adsb.altitude(msg)
        return f"altitude :{alt} feet"
    
    elif 19:
        velocity= pms.adsb.velocity(msg)
        if velocity:
            speed,heading, _,_=velocity
            return f"Speed: {speed} knots, Heading: {heading}°"
        
    elif 20 <= tc <=22:
        return "GNSS position --not decoded"
    
    else:
        return f"unknown message type (TC{tc}): {msg}"