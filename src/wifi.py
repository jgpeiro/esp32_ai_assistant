import time
import network

class Wifi:
    def __init__( self ):
        self.wlan = None
    
    def connect( self, ssid, pswd ):
        self.wlan = network.WLAN( network.STA_IF )
        self.wlan.active( True )
        self.wlan.connect( ssid, pswd )
        while not self.wlan.isconnected():
            time.sleep( 0.1 )
        print( self.wlan.ifconfig() )
    
    def disconnect( self ):
        self.wlan.disconnect()
        self.wlan.active( False )
